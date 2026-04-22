from app.graph.agent_graph import build_agent_graph


workflow=build_agent_graph()

print(workflow.invoke({'input':"I have fever and cough"}))

print(workflow.invoke({'input':'tell me a joke '}))

print(workflow.invoke({'input':'what is fever '}))