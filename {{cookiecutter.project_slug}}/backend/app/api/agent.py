{% if cookiecutter.project_type == 'agent' %}
"""
Agent endpoint
"""
from fastapi import APIRouter
from app.schemas.agent import AgentRequest, AgentResponse

router = APIRouter()

@router.post("/agent", response_model=AgentResponse)
async def run_agent(req: AgentRequest):
    """Execute agent with tools"""
    # TODO: Implement agent logic
    return AgentResponse(result="Implement agent logic", tool_calls=[], reasoning="")
{% endif %}
