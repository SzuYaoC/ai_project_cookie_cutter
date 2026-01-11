"""
Search endpoint
"""
from fastapi import APIRouter
from pydantic import BaseModel
from typing import List, Optional

router = APIRouter()


class SearchRequest(BaseModel):
    query: str
    k: int = 5
    filters: Optional[dict] = None


class SearchResult(BaseModel):
    text: str
    score: float
    metadata: dict


@router.post("/search")
async def search(req: SearchRequest) -> List[SearchResult]:
    """Vector search endpoint - implement via MCP"""
    # TODO: Call MCP search_chunks tool
    return []
