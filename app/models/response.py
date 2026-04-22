from typing import Any

from pydantic import BaseModel


class QuerryResponse(BaseModel):
    output:Any
    intent:str