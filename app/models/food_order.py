import uuid
from datetime import datetime, time, timezone

from sqlalchemy import String, Integer, Numeric, DateTime, Time, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class FoodOrder(Base):
    __tablename__ = "food_orders"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True
    )
    # "room_service" or "dine_in" -- which field below is required
    # depends on this, enforced at the service layer since a plain
    # column constraint can't express "one or the other" cleanly.
    order_type: Mapped[str] = mapped_column(String(20), nullable=False)
    booking_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("bookings.id"), nullable=True
    )
    reservation_time: Mapped[time] = mapped_column(Time, nullable=True)
    status: Mapped[str] = mapped_column(String(20), nullable=False, default="pending")
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )

    items: Mapped[list["FoodOrderItem"]] = relationship(back_populates="food_order")


class FoodOrderItem(Base):
    __tablename__ = "food_order_items"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    food_order_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("food_orders.id"), nullable=False, index=True
    )
    menu_item_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("menu_items.id"), nullable=False
    )
    quantity: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    # Snapshot of MenuItem.price AT THE TIME OF ORDER -- not a live
    # reference. If the restaurant changes a dish's price next week,
    # this historical order must still reflect what the customer
    # actually agreed to pay when they ordered it.
    price_at_order: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)

    food_order: Mapped["FoodOrder"] = relationship(back_populates="items")