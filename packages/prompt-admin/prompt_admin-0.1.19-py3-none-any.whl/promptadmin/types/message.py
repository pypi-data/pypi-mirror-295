from typing import Literal

from pydantic import BaseModel


class Message(BaseModel):
    content: str
    role: Literal['user', 'assistant']
