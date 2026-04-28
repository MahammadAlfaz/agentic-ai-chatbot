
from typing import TypedDict


class AgentState(TypedDict):
    input: str
    intent: str
    output: str
    context: str
    session_id: str