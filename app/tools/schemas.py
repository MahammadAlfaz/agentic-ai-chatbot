from typing import List

from pydantic import BaseModel



class SymptomsOutput(BaseModel):
    conditions:List[str] 
    severity:str
    recommendation:str

class MedicineOutput(BaseModel):
    name:str
    uses:str
    dosage:str
    side_effects:str