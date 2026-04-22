from typing import TypedDict
from langgraph.graph import END, START, StateGraph
from app.llm.llm import get_llm
from app.memory.memory import add_chat, get_history
from app.rag.retriever import get_retriever
from app.tools.tools import get_tools


class AgentState(TypedDict):
    input: str
    intent: str
    output: str
    context: str


def detect_intention(state: AgentState):
    user_input = state["input"].lower()
    if any(word in user_input for word in [
        "what", "define", "explain", "tell me", "about", "causes", "symptoms"
    ]):
        return {"intent": "rag"}

    
    elif any(word in user_input for word in [
        "i have", "fever", "cough", "pain", "headache"
    ]):
        return {"intent": "symptom"}


    elif any(word in user_input for word in [
        "medicine", "drug", "tablet", "paracetamol", "ibuprofen"
    ]):
        return {"intent": "medicine"}

    return {"intent": "general"}


def router(state: AgentState):
    intent = state["intent"]
    if intent in ["symptom", "medicine"]:
        return "tool_node"
    elif intent == "rag":
        return "rag_node"
    else:
        return "llm_node"


def tool_node(state: AgentState):
    tools = get_tools()
    intent = state["intent"]
    user_input = state["input"]

    if intent == "symptom":
        tool = tools[1]
    elif intent == "medicine":
        tool = tools[0]
    else:
        return {"output": "no suitable tool found"}
    result = tool.invoke(user_input)
    return {"output": result}


def llm_node(state: AgentState):
    llm = get_llm()
    user_input = state["input"]
    add_chat("user",user_input)
    history=get_history()
    message=""

    for msg in history:
        message+=f"{msg['role']} : {msg['content']} \n"
    prompt = f"""
    You are a medical assistant having a conversation.

    Conversation history:
    {message}

    Respond appropriately to the latest user query.
    """

    result = llm.invoke(prompt)
    # print("\n",message)
    add_chat("Assistant",result.content)
    return {"output": result.content}


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


def build_agent_graph():
    graph = StateGraph(AgentState)

    graph.add_node("intent_node", detect_intention)
    graph.add_node("tool_node", tool_node)
    graph.add_node("llm_node", llm_node)
    graph.add_node("rag_node", rag_node)

    graph.add_edge(START, "intent_node")
    graph.add_conditional_edges(
        "intent_node",
        router,
        {"llm_node": "llm_node", "tool_node": "tool_node", "rag_node": "rag_node"},
    )
    graph.add_edge("llm_node", END)
    graph.add_edge("tool_node", END)
    graph.add_edge("rag_node", END)
    return graph.compile()
