from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

import schemas
import service
from db import get_db

notification_router = APIRouter()


@notification_router.get("/user/{id}/", summary="User notifications")
def user_notifications(id: int, db: Session = Depends(get_db)):
    """
    Информация об уведомлениях пользователю:

    - **id**: идентификатор пользователя
    """
    return service.get_user_notifications(db, id)



api_router = APIRouter()
api_router.include_router(notification_router, prefix="/notification", tags=["notification"])
