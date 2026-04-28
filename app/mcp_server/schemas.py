

from pydantic import BaseModel


class MedicineResponse(BaseModel):
    name:str
    purpose:str
    dosage:str
    warnings:str
    side_effects:str
    source: str="OpenFDA"