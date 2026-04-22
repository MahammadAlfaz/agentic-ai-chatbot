
from langchain_core.tools import tool
from app.llm.llm import get_llm

@tool
def medicine_info(medicine_name: str) -> str:
 
    """Provide information about a medicine."""
    llm=get_llm()
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
    return response.content