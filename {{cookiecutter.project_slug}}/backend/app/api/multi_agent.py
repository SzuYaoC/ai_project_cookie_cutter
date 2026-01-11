{% if cookiecutter.project_type == 'multi_agent' %}
"""
Multi-agent endpoint
"""
from fastapi import APIRouter
from app.schemas.multi_agent import MultiAgentRequest, MultiAgentResponse

router = APIRouter()

@router.post("/multi-agent", response_model=MultiAgentResponse)
async def run_multi_agent(req: MultiAgentRequest):
    """Execute multi-agent workflow"""
    # TODO: Implement multi-agent logic
    return MultiAgentResponse(result="Implement multi-agent", agent_outputs={}, workflow_log=[])
{% endif %}
