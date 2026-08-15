"""
SQLAlchemy engine + session factory.
DATABASE_URL comes from environment (see app/core/config.py) -- never
hardcoded, so the same code works against local Postgres, docker-compose,
or a managed DB in production just by changing the env var.
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import settings

engine = create_engine(settings.DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    """FastAPI dependency: yields a session, always closes it after the request."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()