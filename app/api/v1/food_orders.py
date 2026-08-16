from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.api.deps import get_current_user
from app.models.user import User
from app.schemas.food_order import FoodOrderCreate, FoodOrderOut
from app.services import food_order_service

router = APIRouter(prefix="/food-orders", tags=["food-orders"])


@router.post("", response_model=FoodOrderOut, status_code=201)
def create_food_order(
    order_in: FoodOrderCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return food_order_service.create_food_order(db, current_user.id, order_in)