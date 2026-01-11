"""
Authentication API Endpoints
"""
from __future__ import annotations
from uuid import uuid4

from fastapi import APIRouter, HTTPException, status, Depends

from sqlalchemy import select, text
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.api.utils.security import verify_user, create_access_token
from app.config import cfg

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login")
async def login(username: str, 
                password: str,
                session:AsyncSession=Depends(get_db)):
    
    current_user = await verify_user(session, username, password)

    if not current_user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid username or password")
    
    ## Create Access Token
    access = create_access_token(sub=str(current_user.id), extra={"role": current_user.role, "username": current_user.username})
    return {
        "user": {"id": current_user.id, "username": current_user.username, "role": current_user.role},
        "tokens": {"access_token": access, "expires_in": cfg.jwt_expire_minutes * 60}
    }