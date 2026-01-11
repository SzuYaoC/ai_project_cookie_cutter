{% if cookiecutter.project_type == 'rag' %}
from pydantic import BaseModel
from typing import List, Optional

class SearchRequest(BaseModel):
    query: str
    k: int = 5
    filters: Optional[dict] = None

class SearchResult(BaseModel):
    text: str
    score: float
    metadata: dict

class AskRequest(BaseModel):
    question: str
    k: int = 5

class Citation(BaseModel):
    title: str
    regulator: str
    text: str

class AskResponse(BaseModel):
    answer: str
    citations: List[Citation]
{% endif %}
