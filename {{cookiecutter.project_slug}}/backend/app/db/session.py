"""
Database session management
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from app.config import cfg


def get_database_url() -> str:
    url = cfg.database_url
    if url.startswith("postgresql://"):
        url = url.replace("postgresql://", "postgresql+psycopg://", 1)
    return url


engine = create_engine(get_database_url(), pool_pre_ping=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
