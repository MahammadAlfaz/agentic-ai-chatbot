import os 
import json

MEMORY_FILE="data/chat_memory"


def get_memory_file(session_id:str)->str:
    os.makedirs(MEMORY_FILE,exist_ok=True)
    return f"{MEMORY_FILE}/{session_id}.json"



def load_memory(session_id:str):
    path=get_memory_file(session_id)
    if not os.path.exists(path):
        return []
    else :
        with open(path,'r') as f:
            return json.load(f)

def save_memory(session_id:str,messages):
    path=get_memory_file(session_id)
    with open(path,'w') as f:
        json.dump(messages,f,indent=2)