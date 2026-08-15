"""
Single declarative Base that every SQLAlchemy model inherits from.
Kept free of model imports to avoid circular imports -- models import
Base from here, so this file must not import models back.
"""
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass