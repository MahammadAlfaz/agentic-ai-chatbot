from typing import Any, Optional

from pydantic import BaseModel


class QuerryResponse(BaseModel):
    output: Optional[Any] = None      
    intent: Optional[str] = None      
    status: Optional[str] = None      
    message: Optional[str] = None    
    session_id: Optional[str] = None