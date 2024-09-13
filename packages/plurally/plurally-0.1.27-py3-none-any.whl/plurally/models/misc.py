import itertools
from typing import Dict, List

from pydantic import BaseModel, field_validator


class Table(BaseModel):
    data: List[Dict[str, str]]

    @field_validator("data", mode="before")
    def check_data(cls, value):
        # make sure everything is a string
        value, other = itertools.tee(value)
        for row in value:
            for key, val in row.items():
                if not isinstance(val, str):
                    row[key] = str(val)
        return other
