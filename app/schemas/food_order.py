import uuid
from datetime import datetime, time
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, field_validator


class FoodOrderItemCreate(BaseModel):
    menu_item_id: uuid.UUID
    quantity: int = 1


class FoodOrderCreate(BaseModel):
    order_type: str  # "room_service" or "dine_in"
    booking_id: uuid.UUID | None = None
    reservation_time: time | None = None
    items: list[FoodOrderItemCreate]

    @field_validator("order_type")
    @classmethod
    def validate_order_type(cls, order_type: str):
        if order_type not in ("room_service", "dine_in"):
            raise ValueError('order_type must be "room_service" or "dine_in"')
        return order_type

    @field_validator("items")
    @classmethod
    def items_not_empty(cls, items: list[FoodOrderItemCreate]):
        if not items:
            raise ValueError("Order must include at least one item")
        return items


class FoodOrderItemOut(BaseModel):
    id: uuid.UUID
    menu_item_id: uuid.UUID
    quantity: int
    price_at_order: Decimal

    model_config = ConfigDict(from_attributes=True)


class FoodOrderOut(BaseModel):
    id: uuid.UUID
    user_id: uuid.UUID
    order_type: str
    booking_id: uuid.UUID | None
    reservation_time: time | None
    status: str
    created_at: datetime
    items: list[FoodOrderItemOut] = []

    model_config = ConfigDict(from_attributes=True)