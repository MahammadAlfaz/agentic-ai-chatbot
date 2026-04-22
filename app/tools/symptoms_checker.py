
from langchain_core.tools import tool

from app.llm.llm import get_llm
from app.tools.schemas import SymptomsOutput


@tool
def symptom_checker(symptoms: str) -> dict:

    """ Analyze patient symptoms and suggest possible conditions."""
    llm=get_llm().with_structured_output(SymptomsOutput)
    prompt = f"""
    You are a medical assistant.

    A patient reports the following symptoms:
    {symptoms}

    1. Suggest possible conditions
    2. Mention severity (low/medium/high)
    3. Suggest next steps (rest / consult doctor)

    Keep the answer short and structured.
    """
    result=llm.invoke(prompt)
    return result.model_dump()