"""
Importing this package registers every model on Base.metadata --
needed so Alembic's autogenerate can see all tables. Add new models
here as you create them.
"""
from app.models.user import User  # noqa: F401