from app.llm.llm import get_llm
from app.rag.rag_state import RagState


def hallucination_grader_node(state:RagState) ->RagState:
    llm=get_llm()
    answer=state['generated_answer']
    docs=state['graded_docs']
    question=state['question']

    if not docs:
        return {'hallucination_score':0.0}
    
    context="\n\n".join(
        [
            f"source {i+1}:\n{doc.page_content}"
            for i,doc in enumerate(docs)
        ]
    )
    prompt = f"""
    You are a medical fact checker. 

    Check if the answer is fully supported by the provided context.
    
    Score the answer between 0.0 and 1.0:
    1.0 → every claim is supported by context
    0.7 → most claims supported, minor gaps
    0.5 → some claims supported, some not
    0.0 → answer is not supported by context at all

    Return ONLY a number between 0.0 and 1.0, nothing else.

    Context:
    {context}

    Question: {question}

    Answer to check:
    {answer}

    Score:
    """
    result = llm.invoke(prompt)

    try:
        score=float(result.content.strip())
        score=max(0.0,min(1.0,score))
    except ValueError:
        score=0.0
    print(f"Hallucination score: {score}")

    return {
        'hallucination_score':score
    }

