import uuid
from typing import Generic, TypeVar, Union

from pydantic import BaseModel
from sqlmodel import Field


ParsedModelType = BaseModel
T = TypeVar('T', bound=ParsedModelType)


class ModelResponse(BaseModel, Generic[T]):
    uuid: str = Field(default_factory=lambda: str(uuid.uuid4()))
    raw_text: str
    parsed_model: Union[T, None] = None
