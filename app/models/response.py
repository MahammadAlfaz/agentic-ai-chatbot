from pydantic import BaseModel


class QuerryResponse(BaseModel):
    output:str
    intent:str