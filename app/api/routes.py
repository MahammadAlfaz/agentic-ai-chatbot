from fastapi import APIRouter
from fastapi.responses import StreamingResponse

from app.graph.agent_graph import build_agent_graph
from app.models.request import QuerryRequest
from app.models.response import QuerryResponse
from app.nodes.intent_node import detect_intent
from app.nodes.stream_node import stream_node


router=APIRouter()


@router.post("/chat",response_model=QuerryResponse)
def chat(request:QuerryRequest):
    workflow=build_agent_graph()
    result=workflow.invoke({
        'input':request.input,
        'session_id':request.session_id
    })
    return QuerryResponse(
       output=result['output'],
       intent=result['intent']
    )
@router.post("/chat/stream")
def stream_response(request:QuerryRequest):
    state = {
        "input": request.input,
        "session_id": request.session_id,
        "intent": "",
        "output": "",
        "context": ""
    }
    state.update(detect_intent(state)
    return StreamingResponse(stream_node(state),media_type="text/event-stream")
