from app.graph.state import AgentState
from app.tools.tools import get_tools


def tool_node(state: AgentState):
    tools = {
        tool.name: tool for tool in get_tools()
        }

    intent = state["intent"]
    user_input = state["input"]

    if intent == "medicine":
        tool = tools.get("medicine_info")
    elif intent == "symptom":
        tool = tools.get("symptom_checker")
    else:
        return {"output": "no suitable tool found"}
    
    if not tool:
        return {"output": f"no suitable tool found for the intent: {intent}"}

    result = tool.invoke(user_input)
    return {"output": result}

