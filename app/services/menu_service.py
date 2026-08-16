"""
Menu listing logic.
"""
from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.models.menu import MenuCategory


def list_menu(db: Session) -> list[MenuCategory]:
    # selectinload eager-loads each category's items in a second query,
    # instead of triggering a separate query per category (N+1 problem)
    # when the response is serialized.
    query = (
        select(MenuCategory)
        .options(selectinload(MenuCategory.items))
        .order_by(MenuCategory.display_order)
    )
    return db.execute(query).scalars().all()