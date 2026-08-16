from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.menu import MenuCategoryOut
from app.services import menu_service

router = APIRouter(prefix="/menu", tags=["menu"])


@router.get("", response_model=list[MenuCategoryOut])
def get_menu(db: Session = Depends(get_db)):
    return menu_service.list_menu(db)