import logging
from typing import Literal, Generic

from anthropic import AsyncAnthropic, NOT_GIVEN
from anthropic.types.message import Message as AnthropicMessage

from promptadmin.prompt_service.models.abstract_streamer import AbstractStreamer
from promptadmin.prompt_service.models.base_model_service import BaseModelService
from promptadmin.types import ModelResponse, Message, ModelServiceInfo
from promptadmin.types.model_response import T
from settings import SETTINGS

logger = logging.getLogger(__name__)


class AnthropicModelResponse(ModelResponse[T], Generic[T]):
    origin_message: AnthropicMessage | None = None
    messages: list[dict[str, str]]


class AnthropicModelService(BaseModelService):
    def __init__(
            self,
            anthropic: AsyncAnthropic = None,
            prompt_position: Literal['system', 'user'] = None,
            max_tokens: int = None,
            model: str = None,
            temperature: float = None
    ):
        self.anthropic = anthropic or AsyncAnthropic(api_key=SETTINGS.anthropic_key)
        self.prompt_position = prompt_position or 'system'
        self.max_tokens = max_tokens or 2048
        self.model = model or 'claude-3-5-sonnet-20240620'
        self.temperature = temperature or NOT_GIVEN

    def info(self) -> ModelServiceInfo:
        return ModelServiceInfo(
            service='anthropic',
            model=self.model,
            config={
                'max_tokens': self.max_tokens,
                'prompt_position': self.prompt_position,
                'temperature': None if self.temperature is NOT_GIVEN else self.temperature
            }
        )

    @staticmethod
    def from_info(model_service_info: ModelServiceInfo):
        return AnthropicModelService(
            prompt_position=model_service_info.config.get('prompt_position'),
            max_tokens=model_service_info.config.get('max_position'),
            model=model_service_info.model,
            temperature=model_service_info.config.get('temperature'),
        )

    async def execute(
            self,
            prompt: str,
            history: list[Message],
            streamer: AbstractStreamer = None
    ) -> AnthropicModelResponse:
        messages = []
        system = NOT_GIVEN
        if self.prompt_position == 'user':
            history.append(Message(content=prompt, role='user'))
        elif self.prompt_position == 'system':
            system = prompt
            if len(history) == 0:
                history.append(Message(content="Hello", role='user'))

        for message in history:
            if message.role == 'user':
                if len(messages) > 0 and messages[-1]['role'] == 'user':
                    messages[-1]['content'] += '\n\n' + message.content
                else:
                    messages.append({'role': 'user', 'content': message.content})
            if message.role == 'assistant':
                if len(messages) <= 0:
                    messages.append({'role': 'user', 'content': 'Hello'})
                if messages[-1]['role'] == 'assistant':
                    messages[-1]['content'] += '\n\n' + message.content
                else:
                    messages.append({'role': 'assistant', 'content': message.content})

        if streamer:
            async with self.anthropic.messages.stream(
                    max_tokens=self.max_tokens,
                    messages=messages,
                    system=system,
                    model=self.model,
                    temperature=self.temperature
            ) as stream:
                async for text in stream.text_stream:
                    await streamer.stream(text)
                anthropic_message = await stream.get_final_message()
        else:
            anthropic_message = await self.anthropic.messages.create(
                max_tokens=self.max_tokens,
                messages=messages,
                system=system,
                model=self.model,
                temperature=self.temperature
            )

        return AnthropicModelResponse(
            raw_text=anthropic_message.content[0].text,
            origin_message=anthropic_message,
            messages=messages
        )
