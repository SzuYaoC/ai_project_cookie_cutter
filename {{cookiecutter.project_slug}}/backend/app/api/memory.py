{% if cookiecutter.project_type == 'chatbot' %}
"""
Memory endpoint
"""
from fastapi import APIRouter
from app.schemas.chat import MemoryRequest, MemoryResponse

router = APIRouter()


@router.post("/memory", response_model=MemoryResponse)
async def memory_op(req: MemoryRequest):
    """Memory operations"""
    # TODO: Implement memory save/retrieve
    return MemoryResponse(success=True, data={"value": req.value})
{% endif %}
