from typing import Dict, List

from app.memory.store import save_memory


chat_memory:List[Dict[str,str]]=[]

def add_chat(role:str,content:str):
    chat_memory.append({
        "role":role,
        "content":content
    })
    save_memory(chat_memory)
def get_history() ->List[Dict[str,str]]:
    return chat_memory