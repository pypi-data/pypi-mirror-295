from .anthropic import AnthropicModelService
from .base_model_service import BaseModelService
from ...types import ModelServiceInfo


def build_model(model_service_info: ModelServiceInfo) -> BaseModelService:
    if model_service_info.service == 'anthropic':
        return AnthropicModelService.from_info(model_service_info)

    raise ValueError()


__all__ = [
    AnthropicModelService,
    build_model
]
