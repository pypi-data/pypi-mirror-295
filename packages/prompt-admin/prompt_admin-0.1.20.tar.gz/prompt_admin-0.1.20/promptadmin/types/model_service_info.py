from pydantic import BaseModel


class ModelServiceInfo(BaseModel):
    service: str
    model: str

    config: dict[str, str | int | float | None]
