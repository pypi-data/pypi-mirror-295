import json
import os
import re
from json import JSONDecodeError
import os.path
from pathlib import Path

from datamodel_code_generator import generate, InputFileType, PythonVersion
import importlib
from tempfile import NamedTemporaryFile
import xmltodict
from pydantic import BaseModel, ValidationError


class ParserOutputService:
    def parse(self, model_type: type[BaseModel], result: str) -> BaseModel | None:
        try:
            return model_type.parse_obj(self.try_extract_json(result))
        except StopIteration:
            pass
        except JSONDecodeError:
            pass
        except ValidationError:
            pass
        try:
            return model_type.parse_obj(self.try_parse_xml(result))
        except ValidationError:
            pass

    def parse_for_json_schema(self, json_schema: dict, result: str) -> dict | None:
        model = self.load_model_from_schema(json_schema)
        if model:
            return self.parse(model, result)

    @staticmethod
    def load_model_from_schema(schema: dict) -> type(BaseModel) | None:
        title = schema['title']

        if not os.path.exists('_models'):
            os.mkdir('_models')
        file_model = NamedTemporaryFile(dir='_models', suffix='.py')

        generate(
            str(schema),
            input_file_type=InputFileType.JsonSchema,
            output=Path(file_model.name),
            target_python_version=PythonVersion.PY_311,
        )

        module = importlib.import_module(f'_models.{file_model.name.split("/")[-1].removesuffix(".py")}')
        model = getattr(module, title)
        return model

    @staticmethod
    def try_extract_json(s: str):
        if '{' not in s and '[' not in s:
            s = '{' + s
        s = s[next(idx for idx, c in enumerate(s) if c in '{['):]
        try:
            return json.loads(s)
        except json.JSONDecodeError as e:
            return json.loads(s[:e.pos])

    @staticmethod
    def try_parse_xml(s: str):
        s = s.replace('\n', '@||')
        tag = re.search(r'<([a-zA-Z_]*)>', s)
        if tag:
            first_tag = tag.group(1)
            res = re.search(rf'<{first_tag}>.*</{first_tag}>', s)
            if res:
                find = res.group(0)
                find = find.replace('@||', '\n')
                return xmltodict.parse(find, attr_prefix='attr_')
        res = re.search(r'<[^>]*/>', s)
        if res is None:
            return None
        find = res.group(0)
        find = find.replace('@||', '\n')
        return xmltodict.parse(find, attr_prefix='attr_')
