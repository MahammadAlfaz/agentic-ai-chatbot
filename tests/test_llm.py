from app.llm.llm import get_llm
model=get_llm()
print(model.invoke("what is ai "))