{% if cookiecutter.project_type == 'chatbot' %}
from pydantic import BaseModel
from typing import List, Optional

class ChatRequest(BaseModel):
    message: str
    history: List[dict] = []

class ChatResponse(BaseModel):
    response: str

class MemoryRequest(BaseModel):
    session_id: str
    key: str
    value: Optional[str] = None

class MemoryResponse(BaseModel):
    success: bool
    data: Optional[dict] = None
{% endif %}
