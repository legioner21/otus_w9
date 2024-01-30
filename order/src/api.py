from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

import schemas
import service
from db import get_db

order_router = APIRouter()


@order_router.post("/", summary="Create order")
def create_order(order_dto: schemas.CreateOrderDto, db: Session = Depends(get_db)):
    """
    Создание заказа:

    - **order_dto**: данные
    """
    return service.create_order(db, order_dto)


api_router = APIRouter()
api_router.include_router(order_router, prefix="/order", tags=["order"])
