import uuid
from datetime import datetime, timezone

from sqlalchemy import String, Integer, Numeric, Text, ForeignKey, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class MenuCategory(Base):
    __tablename__ = "menu_categories"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    # Controls left-to-right / top-to-bottom order on the menu page --
    # without this, category order would depend on insertion order,
    # which admins can't easily control later.
    display_order: Mapped[int] = mapped_column(Integer, nullable=False, default=0)

    items: Mapped[list["MenuItem"]] = relationship(back_populates="category")


class MenuItem(Base):
    __tablename__ = "menu_items"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    category_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("menu_categories.id"), nullable=False, index=True
    )
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    price: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)
    is_available: Mapped[bool] = mapped_column(default=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )

    category: Mapped["MenuCategory"] = relationship(back_populates="items")