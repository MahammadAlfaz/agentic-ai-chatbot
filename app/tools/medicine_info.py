


from langchain.tools import tool


@tool
def medicine_info(medicine_name: str) -> str:
    """
    Provides basic information about medicines.
    """

    med = medicine_name.lower()

    if "paracetamol" in med:
        return "Paracetamol is used to reduce fever and relieve mild pain."

    elif "ibuprofen" in med:
        return "Ibuprofen is a pain reliever and anti-inflammatory drug."

    elif "amoxicillin" in med:
        return "Amoxicillin is an antibiotic used for bacterial infections."

    else:
        return "Medicine information not found. Consult a pharmacist."