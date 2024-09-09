from abc import ABC, abstractmethod


class AbstractStreamer(ABC):
    @abstractmethod
    async def stream(self, text: str):
        pass
