{% if cookiecutter.project_type == 'multi_agent' %}
from pydantic import BaseModel
from typing import List

class MultiAgentRequest(BaseModel):
    task: str
    agents: List[str] = ["researcher", "writer", "critic"]

class MultiAgentResponse(BaseModel):
    result: str
    agent_outputs: dict
    workflow_log: List[str]


{% endif %}
