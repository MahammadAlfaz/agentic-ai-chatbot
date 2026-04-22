from typing import TypedDict

from langgraph.graph import END, START, StateGraph


class GraphState(TypedDict):
    input:str
    output:str


def process_input(state:GraphState):
    input=state['input']

    return {
        'output':f"processed {input}"
    }

def generate_output(state:GraphState):
    result=state['output']

    return {
        'output':f"final answer {result}"
    }

def build_graph():
    graph=StateGraph(GraphState)

    graph.add_node("process_input",process_input)
    graph.add_node("generate_output",generate_output)

    graph.add_edge(START,"process_input")
    graph.add_edge("process_input","generate_output")
    graph.add_edge("generate_output",END)
    return graph.compile()

