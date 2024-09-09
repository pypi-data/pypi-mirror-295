from __future__ import annotations
from abc import abstractmethod

from promptadmin.prompt_service.models.abstract_streamer import AbstractStreamer
from promptadmin.types import Message, ModelResponse, ModelServiceInfo


class BaseModelService:
    @abstractmethod
    async def execute(
            self,
            prompt: str,
            history: list[Message],
            streamer: AbstractStreamer = None
    ) -> ModelResponse:
        """"""

    @abstractmethod
    def info(self) -> ModelServiceInfo:
        """"""
