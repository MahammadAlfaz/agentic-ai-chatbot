from typing import TypedDict

from langgraph.graph import END, START, StateGraph

class AgentState(TypedDict):
    input:str
    intent:str
    output:str

def detect_intention(state:AgentState):
    input=state['input'].lower()

    if 'fever' in input or 'symptom' in input :
        intent='symptom'
    elif 'drug' in input or 'medicine' in input :
        intent ="medicine"
    else :
        intent="general"
    return {'intent':intent}

def router(state:AgentState):
    intent=state['intent']

    if intent =='symptom':
        return "tool_node"
    elif intent =="medicine":
        return 'tool_node'
    else :
        return 'llm_node'
    

def tool_node(state:AgentState):
    return{
        'output':'tool output (placeholder)'
    }

def llm_node(state:AgentState):
    return{
        'output':'llm output(placeholder)'
    }



def build_agent_graph():
    graph=StateGraph(AgentState)

    graph.add_node("intent_node",detect_intention)
    graph.add_node("tool_node",tool_node)
    graph.add_node("llm_node",llm_node)

    graph.add_edge(START,"intent_node")
    graph.add_conditional_edges("intent_node",router,
                                {
                                    "llm_node":"llm_node",
                                    "tool_node":"tool_node"
                                })
    graph.add_edge("llm_node",END)
    graph.add_edge("tool_node",END)
    return graph.compile()