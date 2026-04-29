from langgraph.graph import END, START, StateGraph
from app.graph.state import AgentState
from app.nodes.intent_node import detect_intent
from app.nodes.llm_node import llm_node
from app.nodes.mcp_node import mcp_node
from app.nodes.rag_node import rag_node
from app.nodes.tool_node import tool_node
from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.checkpoint.memory import MemorySaver

checkpointer = MemorySaver()

def router(state: AgentState):
    intent = state["intent"]
    if intent == "medicine":
        return "mcp_node"
    elif intent =='symptom':
        return "tool_node"
    elif intent == "rag":
        return "rag_node"
    else:
        return "llm_node"


def build_agent_graph():
    graph = StateGraph(AgentState)

    graph.add_node("intent_node", detect_intent)
    graph.add_node("tool_node", tool_node)
    graph.add_node("mcp_node",mcp_node)
    graph.add_node("llm_node", llm_node)
    graph.add_node("rag_node", rag_node)

    graph.add_edge(START, "intent_node")
    graph.add_conditional_edges(
        "intent_node",
        router,
        {"llm_node": "llm_node", "tool_node": "tool_node", "rag_node": "rag_node","mcp_node":"mcp_node"},
    )
    graph.add_edge("llm_node", END)
    graph.add_edge("mcp_node",END)
    graph.add_edge("tool_node", END)
    graph.add_edge("rag_node", END)
   
    return graph.compile(checkpointer=checkpointer,interrupt_before=['mcp_node'])
workflow = build_agent_graph()