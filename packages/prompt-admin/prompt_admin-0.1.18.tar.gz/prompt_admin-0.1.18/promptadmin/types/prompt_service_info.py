from pydantic import BaseModel

from promptadmin.types import ModelServiceInfo, Message


class PromptServiceInfo(BaseModel):
    table: str
    field: str
    field_name: str
    name: str | None
    service_model_info: ModelServiceInfo

    template_context_type: dict[str, dict]
    template_context_default: dict[str, dict]

    history_context_default: list[Message] = []

    parsed_model_type: dict | None = None
    parsed_model_default: dict | None = None
    fail_parse_model_strategy: str | None = None
