


from pydantic import BaseModel
import uuid

class QuerryRequest(BaseModel):
    input:str
    session_id:str=str(uuid.uuid4())