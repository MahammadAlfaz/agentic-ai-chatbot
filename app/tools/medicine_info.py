
from langchain_core.tools import tool
from app.llm.llm import get_llm
from app.tools.schemas import MedicineOutput

@tool
def medicine_info(medicine_name: str) -> dict:
 
    """Provide information about a medicine."""
    llm=get_llm().with_structured_output(MedicineOutput)
    prompt = f"""
    You are a medical assistant.

    Provide details about the medicine: {medicine_name}

    Include:
    - Use
    - Dosage (general guidance)
    - Side effects

    Keep it simple and safe.
    """
    response=llm.invoke(prompt)
    return response.model_dump()