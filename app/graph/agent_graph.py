from langgraph.graph import END, START, StateGraph
from app.graph.state import AgentState
from app.llm.llm import get_llm
from app.nodes.intent_node import detect_intent
from app.nodes.llm_node import llm_node
from app.nodes.rag_node import rag_node
from app.nodes.tool_node import tool_node


llm = get_llm()


def router(state: AgentState):
    intent = state["intent"]
    if intent in ["symptom","medicine"]:
        return "tool_node"
    elif intent == "rag":
        return "rag_node"
    else:
        return "llm_node"


def build_agent_graph():
    graph = StateGraph(AgentState)

    graph.add_node("intent_node", detect_intent)
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
