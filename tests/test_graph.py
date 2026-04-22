from app.graph.basic_graph import build_graph


workflow=build_graph()

print(workflow.invoke({"input":"i have fever"}))