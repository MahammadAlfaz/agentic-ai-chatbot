
from app.graph.state import AgentState
from app.llm.llm import get_llm
from app.memory.memory import add_chat, get_history


def stream_node(state: AgentState):
    llm=get_llm()
    user_input = state["input"]
    session_id=state.get("session_id","default")
    add_chat(session_id,"user",user_input)
       
  
    history=get_history(session_id)
    message=""

    for msg in history:
        message+=f"{msg['role']} : {msg['content']} \n"
    prompt = f"""
    You are a medical assistant having a conversation.

    Conversation history:
    {message}

    Respond appropriately to the latest user query.
    """
 

    
    full_response=""
    for chunks in llm.stream(prompt):
        token=chunks.content
        if token :
            full_response+=token
            yield token
    # print("\n",message)
    add_chat(session_id,"Assistant",full_response)
    return {"output": full_response}

