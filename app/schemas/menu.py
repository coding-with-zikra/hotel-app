import uuid
from decimal import Decimal

from pydantic import BaseModel, ConfigDict


class MenuItemOut(BaseModel):
    id: uuid.UUID
    category_id: uuid.UUID
    name: str
    description: str | None = None
    price: Decimal
    is_available: bool

    model_config = ConfigDict(from_attributes=True)


class MenuCategoryOut(BaseModel):
    id: uuid.UUID
    name: str
    display_order: int
    items: list[MenuItemOut] = []

    model_config = ConfigDict(from_attributes=True)