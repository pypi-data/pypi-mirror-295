import logging

import asyncpg
from pydantic import BaseModel

from settings import SETTINGS

logger = logging.getLogger(__name__)


class Variable(BaseModel):
    key: str
    value: str
    template: bool


class VarService:
    def __init__(
            self,
            connection: str = None
    ):
        self.connection = connection or SETTINGS.prompt_admin_settings.var_connection

    async def collect(self) -> list[Variable]:
        try:
            conn = await asyncpg.connect(self.connection)
        except Exception as e:
            logger.error('Error connection database for get vars', exc_info=e)
            return {}

        row = await conn.fetch('SELECT key, value, template FROM pa_var')

        return [
            Variable(
                key=i.get('key'),
                value=i.get('value'),
                template=i.get('template')
            )
            for i in row
        ]

    async def collect_vars(self) -> dict[str, str]:
        try:
            conn = await asyncpg.connect(self.connection)
        except Exception as e:
            logger.error('Error connection database for get vars', exc_info=e)
            return {}

        row = await conn.fetch('SELECT key, value FROM pa_var WHERE template = FALSE')

        return {
            i.get('key'): i.get('value') for i in row
        }

    async def collect_templates(self) -> dict[str, str]:
        try:
            conn = await asyncpg.connect(self.connection)
        except Exception as e:
            logger.error('Error connection database for get vars', exc_info=e)
            return {}

        row = await conn.fetch('SELECT key, value FROM pa_var WHERE template = TRUE')

        return {
            i.get('key'): i.get('value') for i in row
        }

    async def get_var(self, key: str) -> str:
        try:
            conn = await asyncpg.connect(self.connection)
        except Exception as e:
            logger.error('Error connection database for get vars', exc_info=e)
            raise ValueError()

        row = await conn.fetchrow('SELECT value FROM pa_var WHERE key=$1', key)
        var = row.get('value')
        if var is None:
            raise ValueError()
        return var

    async def create(self, key: str, value: str, template: bool):
        try:
            conn = await asyncpg.connect(self.connection)
        except Exception as e:
            logger.error('Error connection database for get vars', exc_info=e)
            return

        await conn.fetch('INSERT INTO pa_var (key, value, template) VALUES ($1, $2, $3)', key, value, template)

    async def change(self, key: str, value: str):
        try:
            conn = await asyncpg.connect(self.connection)
        except Exception as e:
            logger.error('Error connection database for get vars', exc_info=e)
            return

        await conn.fetch('UPDATE pa_var SET value=$1 WHERE key=$2', value, key)

    async def remove(self, key: str):
        try:
            conn = await asyncpg.connect(self.connection)
        except Exception as e:
            logger.error('Error connection database for get vars', exc_info=e)
            return

        await conn.fetch('DELETE FROM pa_var WHERE key=$1', key)
