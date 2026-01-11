{% if cookiecutter.project_type == 'rag' %}
"""
RAG endpoint
"""
from fastapi import APIRouter
from app.schemas.rag import AskRequest, AskResponse

router = APIRouter()

@router.post("/ask", response_model=AskResponse)
async def ask(req: AskRequest):
    """RAG Q&A endpoint"""
    # TODO: Implement RAG workflow
    return AskResponse(answer="Implement RAG logic", citations=[])
{% endif %}
