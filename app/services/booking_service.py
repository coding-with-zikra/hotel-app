"""
Business logic for creating and reading bookings.
"""
import uuid

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.booking import Booking
from app.models.room import Room
from app.schemas.booking import BookingCreate
from app.services.room_service import is_room_available


def create_booking(db: Session, user_id: uuid.UUID, booking_in: BookingCreate) -> Booking:
    room = db.get(Room, booking_in.room_id)
    if room is None or not room.is_active:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Room not found."
        )

    # Re-check availability here, not just at listing time -- the room
    # list the user saw could be stale (another booking may have been
    # made in between them browsing and submitting this request). This
    # is the actual guard against double-booking, done inside a single
    # DB transaction so no other booking can sneak in between the check
    # and the insert.
    if not is_room_available(db, booking_in.room_id, booking_in.check_in, booking_in.check_out):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Room is not available for the selected dates.",
        )

    booking = Booking(
        room_id=booking_in.room_id,
        user_id=user_id,
        check_in=booking_in.check_in,
        check_out=booking_in.check_out,
        status="pending",
    )
    db.add(booking)
    db.commit()
    db.refresh(booking)
    return booking


def get_user_bookings(db: Session, user_id: uuid.UUID) -> list[Booking]:
    return db.execute(
        select(Booking).where(Booking.user_id == user_id).order_by(Booking.check_in)
    ).scalars().all()