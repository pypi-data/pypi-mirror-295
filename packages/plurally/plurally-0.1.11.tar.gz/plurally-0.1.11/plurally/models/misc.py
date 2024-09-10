from typing import Dict, List

from pydantic import BaseModel


class Table(BaseModel):
    data: List[Dict[str, str]]
