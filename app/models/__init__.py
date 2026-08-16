"""
Importing this package registers every model on Base.metadata --
needed so Alembic's autogenerate can see all tables. Add new models
here as you create them.
"""
from app.models.user import User  # noqa: F401
from app.models.room import Room  # noqa: F401
from app.models.booking import Booking  # noqa: F401
from app.models.menu import MenuCategory, MenuItem  # noqa: F401
from app.models.food_order import FoodOrder, FoodOrderItem  # noqa: F401