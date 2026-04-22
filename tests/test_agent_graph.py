from app.graph.agent_graph import build_agent_graph


workflow=build_agent_graph()

print(workflow.invoke({'input':'i have fever'}))

print(workflow.invoke({'input':'tell me a joke '}))