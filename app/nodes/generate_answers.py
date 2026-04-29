from app.llm.llm import get_llm
from app.rag.rag_state import RagState


def generate_answer_node(state:RagState)->RagState:
    llm=get_llm()
    question=state['question']
    docs=state['graded_docs']
    attempts=state.get('attempts',0)

    if not docs:
        return{
            'generated_answer':'I could not find relevant informatiom to answer to you please consult a doctor.',
            'attempts':attempts+1
        
        }
    
    context="\n\n".join([
        f"Source {i+1}:\n{doc.page_content}"
        for i,doc in enumerate(docs)
    ])
    prompt = f"""
    You are a medical assistant. Answer the question using ONLY 
    the provided context. 
    
    If the context doesn't contain enough information, say 
    "I don't have enough information to answer this accurately."
    
    Do NOT make up any medical facts.
    
    Context:
    {context}
    
    Question: {question}
    
    Answer:
    """
    result=llm.invoke(prompt)
    answer=result.content.strip()

    print(f"Generated answer (attempt {attempts+1}) :{answer[:100]}...")

    return {
        "generated_answer":answer,
        "attempts":attempts+1
    }

