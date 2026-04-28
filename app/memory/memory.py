from typing import Dict, List

from app.memory.store import load_memory, save_memory


chat_memory: List[Dict[str, str]] = []


def add_chat(session_id: str, role: str, content: str):
    history = load_memory(session_id)
    history.append({"role": role, "content": content})

    save_memory(session_id, history)


def get_history(session_id: str) -> List[Dict[str, str]]:
    return load_memory(session_id)
