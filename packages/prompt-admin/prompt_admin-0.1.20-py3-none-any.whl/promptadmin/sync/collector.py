from promptadmin.prompt_service.decorator import instances
from promptadmin.types.project_promt_info import ProjectPromptInfo
from settings import SETTINGS


def collect() -> ProjectPromptInfo:
    return ProjectPromptInfo(
        app=SETTINGS.app,
        prompt_service_info=[i.info() for i in instances]
    )
