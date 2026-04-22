from typing import TypedDict

from langgraph.graph import END, START, StateGraph

from app.llm.llm import get_llm
from app.tools.tools import get_tools


class AgentState(TypedDict):
    input: str
    intent: str
    output: str


def detect_intention(state: AgentState):
    input = state["input"].lower()

    if "fever" in input or "symptom" in input:
        intent = "symptom"
    elif "drug" in input or "medicine" in input:
        intent = "medicine"
    else:
        intent = "general"
    return {"intent": intent}


def router(state: AgentState):
    intent = state["intent"]
    if intent == "symptom":
        return "tool_node"
    elif intent == "medicine":
        return "tool_node"
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
    llm=get_llm()
    user_input=state["input"]

    result=llm.invoke(user_input)
    return {
        'output':result.content
    }


def build_agent_graph():
    graph = StateGraph(AgentState)

    graph.add_node("intent_node", detect_intention)
    graph.add_node("tool_node", tool_node)
    graph.add_node("llm_node", llm_node)

    graph.add_edge(START, "intent_node")
    graph.add_conditional_edges(
        "intent_node", router, {"llm_node": "llm_node", "tool_node": "tool_node"}
    )
    graph.add_edge("llm_node", END)
    graph.add_edge("tool_node", END)
    return graph.compile()
