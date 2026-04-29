from fastapi import APIRouter
from fastapi.responses import StreamingResponse

from app.graph.agent_graph import build_agent_graph, workflow
from app.models.request import QuerryRequest
from app.models.response import QuerryResponse
from app.nodes.intent_node import detect_intent
from app.nodes.stream_node import stream_node


router = APIRouter()


@router.post("/chat", response_model=QuerryResponse)
def chat(request: QuerryRequest):

    result = workflow.invoke(
        {"input": request.input, "session_id": request.session_id},
        config={"configurable": {"thread_id": request.session_id}},
    )
    state = workflow.get_state(
        config={"configurable": {"thread_id": request.session_id}}
    )

    if state.next:
        return QuerryResponse( 
            output="pending_approval",
            intent=result['intent'],
            status="pending_approval",
            message="This query requires human approval before proceeding.",
            session_id=request.session_id
        )

    return QuerryResponse(
        output=result['output'],
        intent=result['intent'],
        status="Ok",
        message="Output parsed successfully",
        session_id=request.session_id
    )


@router.get("/chat/history/{session_id}")
def get_chat_history(session_id: str):

    state = workflow.get_state(config={"configurable": {"thread_id": session_id}})

    return {"state": state.values}


@router.post("/chat/stream")
def stream_response(request: QuerryRequest):
    state = {
        "input": request.input,
        "session_id": request.session_id,
        "intent": "",
        "output": "",
        "context": "",
    }
    state.update(detect_intent(state))
    return StreamingResponse(stream_node(state), media_type="text/event-stream")


@router.post("/chat/approve/{session_id}")
def approve_and_resume(session_id: str):
    """Human approved — resume the graph"""

    state = workflow.get_state(config={"configurable": {"thread_id": session_id}})

    if not state.next:
        return {"message": "No pending approval for this session"}

    result = workflow.invoke(None, config={"configurable": {"thread_id": session_id}})

    return QuerryResponse(output=result["output"], intent=result["intent"],status="Ok",
        message="Output parsed successfully",
        session_id=session_id)


@router.post("/chat/reject/{session_id}")
def reject_and_respond(session_id: str):
    """Human rejected — send safe response instead"""

    state = workflow.get_state(config={"configurable": {"thread_id": session_id}})

    if not state.next:
        return {"message": "No pending approval for this session"}

    workflow.update_state(
        config={"configurable": {"thread_id": session_id}},
        values={
            "output": "This query has been reviewed and requires direct consultation with a doctor. Please contact your healthcare provider.",
            "intent": "medicine"     
        },
        as_node="mcp_node",
    )

    return {"message": "Query rejected. Safe response sent to user."}


@router.get("/chat/status/{session_id}")
def get_status(session_id: str):
    """Check if a session is waiting for approval"""

    state = workflow.get_state(config={"configurable": {"thread_id": session_id}})

    return {
        "pending_approval": bool(state.next),
        "waiting_at": list(state.next) if state.next else [],
        "current_input": state.values.get("input", ""),
    }
