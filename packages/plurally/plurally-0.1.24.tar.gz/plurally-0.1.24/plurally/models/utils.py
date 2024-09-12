import os
from typing import List

from pydantic import BaseModel, create_model


def get_required_fields(schema):
    required_fields = set()
    for field_name, field in schema.model_fields.items():
        if field.is_required():
            required_fields.add(field_name)
    return required_fields


class BaseEnvVars(BaseModel):

    @classmethod
    def get_issues(cls):
        issues = []
        for field_name, field in cls.model_fields.items():
            if field.default is None and os.getenv(field_name) is None:
                issues.append(f"Missing required environment variable: {field_name}")
        return issues


def create_dynamic_model(
    model_name: str,
    fields: List[str],
    defaults: dict = None,
    types: dict = None,
    base=None,
):
    fields_map = {}
    defaults = defaults or {}
    types = types or {}
    for field_name in fields:
        field_type = types.get(field_name, str)
        if (
            field_name in defaults
        ):  # do not replace by defaults.get(field_name), as None is not the same as ...
            fields_map[field_name] = (field_type, defaults[field_name])
        else:
            fields_map[field_name] = (field_type, ...)
    return create_model(model_name, **fields_map, __base__=base)
