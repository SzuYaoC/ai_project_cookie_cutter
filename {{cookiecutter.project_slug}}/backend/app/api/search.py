{% if cookiecutter.project_type == 'rag' %}
"""
Search endpoint
"""
from fastapi import APIRouter
from typing import List
from app.schemas.rag import SearchRequest, SearchResult

router = APIRouter()


@router.post("/search", response_model=List[SearchResult])
async def search(req: SearchRequest):
    """Vector search endpoint - implement via MCP"""
    # TODO: Call MCP search_chunks tool or vector DB directly
    return []
{% endif %}
