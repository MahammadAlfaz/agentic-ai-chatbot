from app.graph.state import AgentState
from app.llm.llm import get_llm

llm = get_llm()


def detect_intent(state:AgentState):
    user_input = state["input"]

    prompt = f"""
    You are a router for a medical assistant.

    Classify the user query into one of:
    - rag → needs factual medical explanation
    - medicine → needs  medicine info
    - symptom → need symptom analysis
    - general → normal conversation

    Query: {user_input}

    Return ONLY one word: rag / symptom / general / medicine 
    """

    response = llm.invoke(prompt)

    intent = response.content.strip().lower()

    return {"intent": intent}