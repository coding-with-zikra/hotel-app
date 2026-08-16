"""
Business logic for placing food orders. Handles the room_service vs
dine_in branching, and snapshots each item's price at order time.
"""
import uuid

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.models.food_order import FoodOrder, FoodOrderItem
from app.models.menu import MenuItem
from app.models.booking import Booking
from app.schemas.food_order import FoodOrderCreate


def create_food_order(db: Session, user_id: uuid.UUID, order_in: FoodOrderCreate) -> FoodOrder:
    # Branch validation: each order_type has a different required field.
    # This can't be expressed as a simple DB constraint since it depends
    # on the value of another column, so it's enforced here instead.
    if order_in.order_type == "room_service":
        if order_in.booking_id is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="room_service orders require an active booking_id.",
            )
        booking = db.get(Booking, order_in.booking_id)
        if booking is None or booking.user_id != user_id or booking.status not in ("pending", "confirmed"):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="booking_id must reference your own active booking.",
            )
    elif order_in.order_type == "dine_in":
        if order_in.reservation_time is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="dine_in orders require a reservation_time.",
            )

    order = FoodOrder(
        user_id=user_id,
        order_type=order_in.order_type,
        booking_id=order_in.booking_id if order_in.order_type == "room_service" else None,
        reservation_time=order_in.reservation_time if order_in.order_type == "dine_in" else None,
        status="pending",
    )
    db.add(order)
    db.flush()  # assigns order.id without committing yet

    for item_in in order_in.items:
        menu_item = db.get(MenuItem, item_in.menu_item_id)
        if menu_item is None or not menu_item.is_available:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Menu item {item_in.menu_item_id} is not available.",
            )
        order_item = FoodOrderItem(
            food_order_id=order.id,
            menu_item_id=menu_item.id,
            quantity=item_in.quantity,
            # Snapshot the price NOW -- this order row will always show
            # what the customer actually paid, even if the menu price
            # changes tomorrow.
            price_at_order=menu_item.price,
        )
        db.add(order_item)
    db.commit()

    # Re-query with selectinload instead of relying on refresh() --
    # more explicit and reliable for loading a relationship collection
    # after inserting related rows in the same transaction.
    return db.execute(
        select(FoodOrder).options(selectinload(FoodOrder.items)).where(FoodOrder.id == order.id)
    ).scalar_one()