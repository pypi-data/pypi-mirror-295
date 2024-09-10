from pydantic import BaseModel

from promptadmin.types import PromptServiceInfo


class ProjectPromptInfo(BaseModel):
    app: str
    prompt_service_info: list[PromptServiceInfo]
