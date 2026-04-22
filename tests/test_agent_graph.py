from app.graph.agent_graph import build_agent_graph


workflow=build_agent_graph()

# print(workflow.invoke({'input':"I have fever and cough"}),'\n')


##LLM
print(workflow.invoke({'input': 'hi i am new patient alfaz i am 21 years old '}),'\n')
print(workflow.invoke({'input': 'who am i '}),'\n')
print(workflow.invoke({'input': 'how old am i  '}),'\n')

# print(workflow.invoke({'input':'what is heart attack  '}),'\n')