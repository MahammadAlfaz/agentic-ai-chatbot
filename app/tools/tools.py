from app.tools.medicine_info import medicine_info
from app.tools.symptoms_checker import symptom_checker


def get_tools():
    return [
        medicine_info,
        symptom_checker
    ]