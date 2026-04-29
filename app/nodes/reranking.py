from app.llm.llm import get_llm
from app.rag.rag_state import RagState


def reranking_node(state:RagState)->RagState:
    llm=get_llm()
    question=state['question']
    docs=state['retrieved_docs']

    if not docs:
        print("No docs to rerank")
        return {'retrieved_docs':[]}
    scored_docs=[]
    for doc in docs:
        prompt = f"""
        Score how relevant this document is to the question.
        Return ONLY a number between 0.0 and 1.0.
        
        Question: {question}
        
        Document: {doc.page_content[:500]}
        
        Relevance score (0.0 to 1.0):
        """

        result = llm.invoke(prompt)

        try:
            score=float(result.content.strip())
            score=max(0.0,min(1.0,score))
        except ValueError:
            score=0.0

        print(f"Doc score :{score} | {doc.page_content[:80]}...")
        scored_docs.append((score,doc))
    scored_docs.sort(key=lambda x: x[0], reverse=True)
    top_docs=[doc for score,doc in scored_docs[:3]]

    print(f"Top {len(top_docs)} docs after reranking")

    return {
        'retrieved_docs':top_docs
    }

    