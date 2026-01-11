"""
Database models
"""
from uuid import UUID, uuid4
from datetime import datetime
from typing import Optional

from sqlalchemy import String, Boolean, TIMESTAMP, func, Text
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase

class Base(DeclarativeBase):
    pass

class UserInfo(Base):
    """User authentication model - maps to users_info table"""
    __tablename__ = "users_info"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    username: Mapped[str] = mapped_column(Text, nullable=False, unique=True)
    password_hash: Mapped[str] = mapped_column(Text, nullable=False)
    role: Mapped[str] = mapped_column(Text, nullable=False, default="user")
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), server_default=func.now(), nullable=False)
