import inspect
import logging
from typing import Callable, Awaitable, Any, get_args

from jinja2.nativetypes import NativeEnvironment
from polyfactory.factories.pydantic_factory import ModelFactory
from pydantic import BaseModel

from promptadmin.output.parser_output_service import ParserOutputService
from promptadmin.prompt_service.models.base_model_service import BaseModelService, Message, ModelResponse
from promptadmin.types import PromptServiceInfo
from promptadmin.vars.var_service import VarService

logger = logging.getLogger(__name__)


class InspectPromptService:
    def __init__(
            self,
            table: str,
            field: str,
            field_name: str,
            name: str | None,
            func: Callable[[Any, Any], Awaitable[Any]],
            model_service: BaseModelService,
            template_context_default: dict[str, BaseModel],
            parser_output_service: ParserOutputService = None,
            history_context_default: list[Message] = None,
            parsed_model_default: dict = None,
            fail_parse_model_strategy: str = None,
            var_service: VarService = None
    ):
        self.table = table
        self.field = field
        self.field_name = field_name
        self.name = name
        self.func = func
        self.model_service = model_service
        self.template_context_type = {}
        self.template_context_default = template_context_default
        self.parsed_model_type = None
        self.parser_output_service = parser_output_service or ParserOutputService()
        self.history_context_default = history_context_default or []
        self.parsed_model_default = parsed_model_default
        self.fail_parse_model_strategy = fail_parse_model_strategy
        self.var_service = var_service or VarService()

        self.collect_template_context_type()
        self.collect_parsed_model_type()

    def info(self) -> PromptServiceInfo:
        parsed_model_default = self.parsed_model_default
        if parsed_model_default is None and self.parsed_model_type:
            parsed_model_default = ModelFactory.create_factory(self.parsed_model_type).build().model_dump()
        return PromptServiceInfo(
            table=self.table,
            field=self.field,
            field_name=self.field_name,
            name=self.name,
            service_model_info=self.model_service.info(),
            template_context_type=dict(
                (k, v.model_json_schema(mode='serialization')) for k, v in self.template_context_type.items()
            ),
            template_context_default={
                **{
                    k: v.dict() for k, v in self.template_context_default.items()
                },
                **{
                    k: ModelFactory.create_factory(v).build().model_dump() for k, v in
                    self.template_context_type.items()
                    if k not in self.template_context_default
                }
            },
            history_context_default=self.history_context_default,
            parsed_model_type=self.parsed_model_type.model_json_schema(
                mode='serialization') if self.parsed_model_type else None,
            parsed_model_default=parsed_model_default,
            fail_parse_model_strategy=self.fail_parse_model_strategy
        )

    def collect_template_context_type(self):
        for k, v in inspect.getfullargspec(self.func).annotations.items():
            if k == 'return' or k == 'history':
                continue
            if issubclass(v, BaseModel):
                self.template_context_type[k] = v

    def collect_parsed_model_type(self):
        for k, v in inspect.getfullargspec(self.func).annotations.items():
            if k != 'return':
                continue

            return_type = get_args(v.model_fields['parsed_model'].annotation)[0]
            if str(return_type) == '~T':
                continue
            self.parsed_model_type = return_type

    async def process(
            self,
            *args,
            prompt: str | None = None,
            history: list[Message] | None = None,
            mapping_name: str | None = None,
            **kwargs
    ) -> ModelResponse:
        """

        :param args:
        :param prompt:
        :param history:
        :param mapping_name: For logging
        :param kwargs:
        :return:
        """
        contexts = self._collect_contexts(*args, **kwargs)
        prompt = await self._collect_prompt(prompt, contexts)
        history = history or []
        return await self._execute_prompt(prompt, history, mapping_name)

    def _collect_contexts(self, *args, **kwargs):
        contexts = {}
        for v in args:
            for k, v1 in self.template_context_type.items():
                if isinstance(v, v1):
                    contexts[k] = v

        for k, v in kwargs.items():
            for k1, v1 in self.template_context_type.items():
                if isinstance(v, v1):
                    if k == k1:
                        contexts[k] = v

        if len(self.template_context_type) != len(contexts):
            raise ValueError()
        return contexts

    async def _collect_prompt(self, prompt: str | None, contexts) -> str:
        if prompt is None:
            if self.name is None:
                raise ValueError()
            raise NotImplementedError()

        environment = NativeEnvironment(autoescape=True, enable_async=True)
        template_ = environment.from_string(prompt)

        var = await self._collect_vars()

        contexts.update(
            {'var': var}
        )

        async def render_template(template_key: str):
            templ = await self.var_service.get_var(template_key)
            templ_ = environment.from_string(templ)
            return await templ_.render_async(
                **contexts,
                render_template=render_template
            )

        return await template_.render_async(
            **contexts,
            render_template=render_template
        )

    async def _collect_vars(self) -> dict[str, str]:
        return await self.var_service.collect_vars()

    async def _collect_templates(self) -> dict[str, str]:
        return await self.var_service.collect_templates()

    async def _execute_prompt(
            self,
            prompt: str,
            history: list[Message],
            mapping_name: str | None = None,
    ) -> ModelResponse:
        model_response = await self.model_service.execute(prompt, history)

        try:
            if self.parsed_model_type:
                model_response.parsed_model = self.parser_output_service.parse(
                    self.parsed_model_type,
                    model_response.raw_text
                )
                if model_response.parsed_model is None:
                    if self.fail_parse_model_strategy == 'exception':
                        raise ValueError()
                    elif self.fail_parse_model_strategy == 'default':
                        model_response.parsed_model = self.parsed_model_default
        finally:
            logger.info(
                'Model processing',
                extra={
                    'prompt': prompt,
                    'history': history,
                    'mapping': {
                        'table': self.table,
                        'field': self.field,
                        'field_name': self.field_name,
                        'name': mapping_name or self.name,
                    },
                    'model': {
                        'config': self.model_service.info().model_dump(),
                        'response': model_response.model_dump(),
                    },
                    'parsing': {
                        'parsed_model_type': str(self.parsed_model_type),
                        'raw_text': str(model_response.raw_text),
                        'parsed_model': str(model_response.parsed_model)
                    }
                }
            )

        return model_response
