from typing import Awaitable, Callable, Any, Literal

from pydantic import BaseModel

from promptadmin.prompt_service.inspect_prompt_service import InspectPromptService
from promptadmin.prompt_service.models.anthropic import AnthropicModelService
from promptadmin.prompt_service.models.base_model_service import BaseModelService, ModelResponse
from promptadmin.types import Message

instances: list[InspectPromptService] = []


def bind_prompt(
        table: str,
        field: str,
        field_name: str,
        name: str | None = None,
        model_service: BaseModelService | None = None,
        template_context_default: dict[str, BaseModel] | None = None,
        history_context_default: list[Message] = None,
        parsed_model_default: BaseModel | dict = None,
        fail_parse_model_strategy: Literal['exception', 'default'] | None = None
):
    model_service = model_service or AnthropicModelService()
    template_context_default = template_context_default or {}
    history_context_default = history_context_default or []

    def bind_prompt_wrapper(func: Callable[[Any, Any], Awaitable[Any]]):
        inspect_prompt_service = InspectPromptService(
            table,
            field,
            field_name,
            name,
            func,
            model_service=model_service,
            template_context_default=template_context_default,
            history_context_default=history_context_default,
            parsed_model_default=parsed_model_default,
            fail_parse_model_strategy=fail_parse_model_strategy
        )
        instances.append(inspect_prompt_service)

        async def wrapper(
                self,
                *args,
                prompt: str | None = None,
                history: list[Message] | None = None,
                **kwargs
        ) -> ModelResponse:
            return await inspect_prompt_service.process(*args, prompt=prompt, history=history, **kwargs)

        return wrapper

    return bind_prompt_wrapper
