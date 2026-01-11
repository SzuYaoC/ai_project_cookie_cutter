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
# from app.api import auth, ask, search
# app.include_router(auth.router, prefix="/auth", tags=["auth"])
# app.include_router(ask.router, tags=["rag"])
# app.include_router(search.router, tags=["search"])


@app.get("/health")
async def health():
    return {"status": "ok"}
