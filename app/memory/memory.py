from typing import Dict, List


chat_memory:List[Dict[str,str]]=[]

def add_chat(role:str,content:str):
    chat_memory.append({
        "role":role,
        "content":content
    })
def get_history() ->List[Dict[str,str]]:
    return chat_memory