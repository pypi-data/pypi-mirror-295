from fastapi import APIRouter, Request, BackgroundTasks
from pydantic import BaseModel

from promptadmin.sync.collector import collect
from promptadmin.sync.status_monitor.test_load_service import TestLoadService
from promptadmin.sync.status_monitor.test_run_service import TestRunService
from promptadmin.types import ProjectPromptInfo
from settings import SETTINGS

router = APIRouter(prefix='/prompt-admin')

test_run_service = TestRunService()
test_load_service = TestLoadService()


class TestCaseResponse(BaseModel):
    test_case: dict | None


@router.get('/collect', response_model=ProjectPromptInfo)
async def get_collect(request: Request):
    if request.headers.get('Prompt-Admin-Secret', None) != SETTINGS.prompt_admin_settings.router_secret:
        raise ValueError()
    return collect()


@router.get('/status/run_test')
async def status_run_test(request: Request, background_tasks: BackgroundTasks):
    if request.headers.get('Prompt-Admin-Secret', None) != SETTINGS.prompt_admin_settings.router_secret:
        raise ValueError()
    background_tasks.add_task(test_run_service.run_test)


@router.get('/status/test_list', response_model=dict[str, float])
async def status_test_list(request: Request):
    if request.headers.get('Prompt-Admin-Secret', None) != SETTINGS.prompt_admin_settings.router_secret:
        raise ValueError()
    return await test_load_service.list()


@router.get('/status/test/{uuid}', response_model=TestCaseResponse)
async def status_test_load(request: Request, uuid: str):
    if request.headers.get('Prompt-Admin-Secret', None) != SETTINGS.prompt_admin_settings.router_secret:
        raise ValueError()
    return TestCaseResponse(
        test_case=await test_load_service.load(uuid)
    )
