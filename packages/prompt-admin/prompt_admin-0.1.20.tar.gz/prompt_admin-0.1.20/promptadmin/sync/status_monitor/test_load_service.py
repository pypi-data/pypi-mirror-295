import json
import os.path


class TestLoadService:
    @staticmethod
    async def list() -> dict[str, float]:
        if not os.path.exists('test_reports'):
            return {}
        response = {}
        for i in os.listdir('test_reports'):
            try:
                with open(f'test_reports/{i}', 'r') as file:
                    file_json = json.loads(file.read())
                    response[i.removesuffix('.json')] = file_json['created']
            finally:
                pass
        return response

    @staticmethod
    async def load(uuid: str) -> dict | None:
        if not os.path.exists('test_reports'):
            return
        try:
            with open(f'test_reports/{uuid}.json', 'r') as file:
                return json.loads(file.read())
        finally:
            pass
