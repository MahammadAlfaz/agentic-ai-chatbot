from fastapi import APIRouter

from app.graph.agent_graph import build_agent_graph
from app.models.request import QuerryRequest
from app.models.response import QuerryResponse


router=APIRouter()


@router.post("/chat",response_model=QuerryResponse)
def chat(request:QuerryRequest):
    workflow=build_agent_graph()
    result=workflow.invoke({
        'input':request.input
    })
    return QuerryResponse(
       output=result['output'],
       intent=result['intent']
    )
