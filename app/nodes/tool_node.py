from app.graph.state import AgentState
from app.tools.tools import get_tools


def tool_node(state: AgentState):
    tools = get_tools()
    intent = state["intent"]
    user_input = state["input"]

    if intent == "medicine":
        tool = tools[0]
    elif intent == "symptom":
        tool = tools[1]
    else:
        return {"output": "no suitable tool found"}
    result = tool.invoke(user_input)
    return {"output": result}

