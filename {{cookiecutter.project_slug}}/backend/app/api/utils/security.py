from fastapi import HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from uuid import UUID
from jose import jwt, JWTError
import time
from typing import Optional, Dict, Any
from app.config import cfg
from app.db.models import UserInfo
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select





async def verify_user(session: AsyncSession, username: str, password: str) -> Optional[UserInfo]:
    result = await session.execute(
        select(UserInfo).where(UserInfo.username == username)
    )

    current_user = result.scalar_one_or_none()
    if not current_user:
        return None
    
    if current_user.password_hash != password:
        return None
        
    return current_user


def create_access_token(sub: str, extra: Optional[Dict[str, Any]]=None) -> str:
    payload: Dict[str, Any] = {
        "sub": sub,
        "type": "access",
        "exp": int(time.time()) + (cfg.jwt_expire_minutes * 60),
        "iat": int(time.time()),
    }
    if extra:
        payload.update(extra)
    return jwt.encode(payload, cfg.jwt_secret_key, algorithm=cfg.jwt_algorithm)



def decode_token(token: str) -> Dict[str, Any]:
    try:
        return jwt.decode(token, cfg.jwt_secret_key, algorithms=[cfg.jwt_algorithm])
    except JWTError as e:
        raise ValueError("Invalid token") from e



bearer = HTTPBearer()
async def get_current_user(creds: HTTPAuthorizationCredentials = Depends(bearer))->dict:
    token = creds.credentials
    try:
        payload =  decode_token(token)
        return payload
    except ValueError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not an access token")

    

