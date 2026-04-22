from openai import BaseModel


class QuerryRequest(BaseModel):
    input:str