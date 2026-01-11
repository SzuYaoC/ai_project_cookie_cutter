{% if cookiecutter.project_type == 'chatbot' %}
"""
Chat endpoint
"""
from fastapi import APIRouter
from app.schemas.chat import ChatRequest, ChatResponse

router = APIRouter()

@router.post("/chat", response_model=ChatResponse)
async def chat(req: ChatRequest):
    """Simple chat endpoint"""
    # TODO: Implement chat logic with LLM
    return ChatResponse(response="Implement chat logic")
{% endif %}
