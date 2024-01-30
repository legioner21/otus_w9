from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

import schemas
import service
from db import get_db

user_router = APIRouter()


@user_router.post("/", summary="Create user")
def create_user(user_dto: schemas.CreateUserDto, db: Session = Depends(get_db)):
    """
    Создание пользователя:

    - **username**: логин
    """
    return service.create_user(db, user_dto)


@user_router.get("/{id}/", summary="User info")
def create_user(id: int, db: Session = Depends(get_db)):
    """
    Информация о пользователе:

    - **id**: идентификатор пользователя
    """
    return service.get_user_by_id(db, id)


@user_router.post("user/put/money/", summary="Put money")
def create_user(data: schemas.BalanceDto, db: Session = Depends(get_db)):
    """
    Положить на счет пользователя деньги :

    - **user_id**: id пользователя
    - **amount**: сумма
    """
    return service.user_put_money(db, data)


api_router = APIRouter()
api_router.include_router(user_router, prefix="/user", tags=["user"])
