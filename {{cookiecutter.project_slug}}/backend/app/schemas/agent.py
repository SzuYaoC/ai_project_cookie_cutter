{% if cookiecutter.project_type == 'agent' %}
from pydantic import BaseModel
from typing import List

class AgentRequest(BaseModel):
    task: str
    tools: List[str] = []

class AgentResponse(BaseModel):
    result: str
    tool_calls: List[dict]
    reasoning: str
{% endif %}
