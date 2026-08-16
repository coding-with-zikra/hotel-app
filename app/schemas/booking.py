import uuid
from datetime import date, datetime

from pydantic import BaseModel, ConfigDict, field_validator


class BookingCreate(BaseModel):
    room_id: uuid.UUID
    check_in: date
    check_out: date

    @field_validator("check_out")
    @classmethod
    def check_out_after_check_in(cls, check_out: date, info):
        check_in = info.data.get("check_in")
        # Catches the obvious bad input (checkout before/on checkin) here,
        # at the schema layer, before it ever reaches the DB or the
        # overlap-checking logic in the service.
        if check_in and check_out <= check_in:
            raise ValueError("check_out must be after check_in")
        return check_out


class BookingOut(BaseModel):
    id: uuid.UUID
    room_id: uuid.UUID
    user_id: uuid.UUID
    check_in: date
    check_out: date
    status: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)