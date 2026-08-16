import uuid
from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict


class RoomBase(BaseModel):
    name: str
    description: str | None = None
    price_per_night: Decimal
    capacity: int = 2


class RoomCreate(RoomBase):
    pass


class RoomOut(RoomBase):
    id: uuid.UUID
    is_active: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)