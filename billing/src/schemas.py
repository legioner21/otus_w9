from decimal import Decimal
from typing import Dict, Optional

from pydantic import BaseModel, Field


class UserBase(BaseModel):
    username: str
    balance: Decimal


class CreateUserDto(BaseModel):
    username: str


class UserDto(UserBase):
    id: int

    class Config:
        orm_mode = True


class BalanceDto(BaseModel):
    user_id: int
    amount: Decimal = Field(None, ge=1)


class RqSendDataDto(BaseModel):
    queue: str
    message: Dict
    correlation_id: Optional[str]
    reply_to: Optional[str]