
from app.graph.state import AgentState
from app.llm.llm import get_llm
from app.memory.memory import add_chat, get_history

llm=get_llm()
def llm_node(state: AgentState):
    user_input = state["input"]
    add_chat("user",user_input)
    history=get_history()
    message=""

    for msg in history:
        message+=f"{msg['role']} : {msg['content']} \n"
    prompt = f"""
    You are a medical assistant having a conversation.

    Conversation history:
    {message}

    Respond appropriately to the latest user query.
    """

    result = llm.invoke(prompt)
    # print("\n",message)
    add_chat("Assistant",result.content)
    return {"output": result.content}

