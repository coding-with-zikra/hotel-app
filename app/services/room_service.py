"""
Room listing + availability logic. This is the core business rule of
the whole booking system: a room is available for a date range if NO
existing (non-cancelled) booking overlaps that range.
"""
from datetime import date

from sqlalchemy import select, and_, or_
from sqlalchemy.orm import Session

from app.models.room import Room
from app.models.booking import Booking

# Bookings in these statuses hold a room -- cancelled bookings free it up.
BLOCKING_STATUSES = ("pending", "confirmed")


def list_rooms(
    db: Session,
    check_in: date | None = None,
    check_out: date | None = None,
    guests: int | None = None,
    min_price: float | None = None,
    max_price: float | None = None,
) -> list[Room]:
    query = select(Room).where(Room.is_active.is_(True))

    if guests is not None:
        query = query.where(Room.capacity >= guests)
    if min_price is not None:
        query = query.where(Room.price_per_night >= min_price)
    if max_price is not None:
        query = query.where(Room.price_per_night <= max_price)

    # Date filtering needs the overlap logic, so it's handled separately
    # below rather than as a simple WHERE clause on this query.
    rooms = db.execute(query).scalars().all()

    if check_in and check_out:
        rooms = [r for r in rooms if is_room_available(db, r.id, check_in, check_out)]

    return rooms


def is_room_available(db: Session, room_id, check_in: date, check_out: date) -> bool:
    """
    Two date ranges [a_start, a_end) and [b_start, b_end) overlap iff:
        a_start < b_end AND a_end > b_start

    Applied here: an existing booking conflicts with the requested range if
        existing.check_in  < requested.check_out
        AND
        existing.check_out > requested.check_in

    This is the standard interval-overlap test -- it correctly rejects
    same-day-touching ranges too (e.g. an existing booking ending on the
    15th does NOT conflict with a new booking starting on the 15th, since
    hotel days are exclusive of the checkout date).
    """
    conflict_exists = db.execute(
        select(Booking.id).where(
            and_(
                Booking.room_id == room_id,
                Booking.status.in_(BLOCKING_STATUSES),
                Booking.check_in < check_out,
                Booking.check_out > check_in,
            )
        )
    ).first()

    return conflict_exists is None