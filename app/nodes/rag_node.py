from app.graph.state import AgentState
from app.llm.llm import get_llm
from app.rag.retriever import get_retriever

USE_ADVANCED_RAG=True
def rag_node(state: AgentState):
    if USE_ADVANCED_RAG:
        from app.graph.rag_graph import rag_workflow
        question=state['input']
        result=rag_workflow.invoke({
            'question':question,
            'transformed_querry':"",
            'should_retrieve':True,
            "retrieved_docs":[],
            "graded_docs":[],
            'web_search_used':False,
            "generated_answer":"",
            "hallucination_score":0.0,
            "attempts":0,
            "final_answer":""
        })
        return{
            "output":result.get("generated_answer","I could not find relevant information.")
        }
    llm = get_llm()
    retriever = get_retriever()

    user_input = state["input"]
    docs = retriever.invoke(user_input)

    context = "\n".join([document.page_content for document in docs])
    prompt = f"""
        You are a medical assistant.

        Answer ONLY from the provided context.
        If the answer is not clearly present, say "I don't know".

        Be precise and short.

        Context:
        {context}

        Question:
        {user_input}
        """
    result = llm.invoke(prompt)

    return {"output": result.content, "context": context}