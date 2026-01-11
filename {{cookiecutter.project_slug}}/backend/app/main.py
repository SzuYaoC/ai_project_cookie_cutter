"""
FastAPI main application
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="{{ cookiecutter.project_name }}", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Import routers
from app.api.utils import auth
app.include_router(auth.router, tags=["auth"])

{% if cookiecutter.project_type == 'rag' %}
from app.api import rag, search
app.include_router(rag.router, tags=["rag"])
app.include_router(search.router, tags=["search"])
{% endif %}

{% if cookiecutter.project_type == 'chatbot' %}
from app.api import chat, memory
app.include_router(chat.router, tags=["chat"])
app.include_router(memory.router, tags=["memory"])
{% endif %}

{% if cookiecutter.project_type == 'agent' %}
from app.api import agent
app.include_router(agent.router, tags=["agent"])
{% endif %}

{% if cookiecutter.project_type == 'multi_agent' %}
from app.api import multi_agent
app.include_router(multi_agent.router, tags=["multi-agent"])
{% endif %}


@app.get("/health")
async def health():
    return {"status": "ok"}
