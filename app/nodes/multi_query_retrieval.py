from app.llm.llm import get_llm
from app.rag.rag_state import RagState
from app.rag.retriever import get_retriever


def multi_query_retrieval_node(state:RagState)->RagState:
    llm=get_llm()
    transformed_query=state['transformed_querry']
    prompt = f"""
    Generate 4 different search queries to find medical information 
    about the following topic.
    
    Each query should focus on a different aspect.
    Return ONLY the 4 queries, one per line, no numbering, no extra text.
    
    Topic: {transformed_query}
    
    Queries:
    """
    result=llm.invoke(prompt)
    queries =[
        q.strip()
        for q in result.content.strip().split("\n")
        if q.strip()
    ][:4]
    print(f"Generated queries: {queries}")

    retriever=get_retriever()
    all_docs=[]
    seen_content=set()

    for query in queries:
        docs=retriever.invoke(query)
        for doc in docs:
            if doc.page_content not in seen_content:
                seen_content.add(doc.page_content)
                all_docs.append(doc)
    print(f"total unique docs retrieved {len(all_docs)}")
    return {
        "retrieved_docs":all_docs
    }
    
