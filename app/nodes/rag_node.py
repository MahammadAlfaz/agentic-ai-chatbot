from app.graph.state import AgentState
from app.llm.llm import get_llm
from app.rag.retriever import get_retriever


def rag_node(state: AgentState):
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