from app.llm.llm import get_llm
from app.rag.rag_state import RagState


def query_transform_node(state:RagState) -> RagState:
    llm=get_llm()
    question= state['question']
    prompt = f"""
    You are an expert at reformulating medical questions for better search results.
    
    Rewrite the following question to be more specific and search friendly.
    Return ONLY the rewritten query, nothing else.
    
    Original question: {question}
    
    Rewritten query:
    """
    result=llm.invoke(prompt)
    transformed =result.content.strip()

    print(f"original querry: {question}")
    print(f"transformed querry: {transformed}")
    return {'transformed_querry':transformed}
