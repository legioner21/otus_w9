import enum
from decimal import Decimal
from typing import Dict, Optional

from pydantic import BaseModel


class BaseOrderDto(BaseModel):
    user_id: int
    price: Decimal


class CreateOrderDto(BaseOrderDto):
    pass


class OrderDto(BaseOrderDto):
    id: int

    class Config:
        orm_mode = True


class OrderState(str, enum.Enum):
    CREATED = "created"
    PAYMENT = "payment"
    SUCCESS_COMPLETED = "success_completed"
    ERROR_COMPLETED = "error_completed"


class RqSendDataDto(BaseModel):
    queue: str
    message: Dict
    correlation_id: Optional[str]
    reply_to: Optional[str]