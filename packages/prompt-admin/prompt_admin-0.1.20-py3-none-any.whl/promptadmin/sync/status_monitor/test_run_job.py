import asyncio

from promptadmin.sync.status_monitor.test_run_service import TestRunService
from settings import SETTINGS


class TestRunJob:
    def __init__(self, test_run_service: TestRunService = None):
        self.test_run_service = test_run_service or TestRunService()

    async def start(self):
        await asyncio.sleep(20)
        while True:
            self.test_run_service.run_test()
            await asyncio.sleep(SETTINGS.prompt_admin_settings.test_rerun_timeout)

    async def stop(self):
        pass
