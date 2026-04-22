from typing import List

from openai import BaseModel


class SymptomsOutput(BaseModel):
    condition:List[str]
    severity:str
    recommendation:str

class MedicineOutput(BaseModel):
    name:str
    uses:str
    dosage:str
    side_effects:str