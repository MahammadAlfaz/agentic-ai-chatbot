from app.llm.llm import get_llm
from app.rag.rag_state import RagState


def should_retrieve_node(state:RagState)->RagState:
    llm=get_llm()
    question=state['transformed_querry']
    prompt = f"""
    You are a medical assistant deciding if a question needs 
    document retrieval to answer accurately.

    Return ONLY "yes" or "no".

    "yes" → question needs medical facts, drug info, 
             symptoms, treatments, or specific medical knowledge
    "no"  → question is conversational, simple math, 
             greetings, or general knowledge

    Question: {question}

    Answer (yes/no):
    """
    result=llm.invoke(prompt)
    decision=result.content.strip().lower()

    should_retrieve="yes" in decision

    print(f"Should retrieve: {should_retrieve}")
    return{
        "should_retrieve":should_retrieve,
        "attempts":0
    }
