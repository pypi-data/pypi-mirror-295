import os

from pydantic import BaseModel


class PromptAdminSettings(BaseModel):
    router_secret: str = os.getenv('PROMPT_ADMIN_ROUTER_SECRET')
    var_connection: str = os.getenv('PROMPT_ADMIN_VAR_CONNECTION')
    test_rerun_timeout: int = 60 * 60 * 6


class Settings(BaseModel):
    prompt_admin_settings: PromptAdminSettings = PromptAdminSettings()
