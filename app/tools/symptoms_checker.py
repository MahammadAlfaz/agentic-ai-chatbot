
from langchain.tools import tool


@tool
def symptom_checker(symptoms: str) -> str:
    """
    Takes symptoms as input and returns possible conditions.
    """

    symptoms = symptoms.lower()

    if "fever" in symptoms and "cough" in symptoms:
        return "Possible conditions: Flu, COVID-19"

    elif "headache" in symptoms and "nausea" in symptoms:
        return "Possible conditions: Migraine"

    elif "chest pain" in symptoms:
        return "Possible condition: Heart-related issue (consult doctor immediately)"

    else:
        return "Condition unclear. Please consult a doctor."