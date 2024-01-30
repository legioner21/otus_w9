from typing import Dict, Optional

from pydantic import BaseModel


class NotificationBase(BaseModel):
    user_id: int
    order_id: int
    text: str


class CreateNotificationDto(NotificationBase):
    pass


class NotificationDto(NotificationBase):
    id: int

    class Config:
        orm_mode = True


class RqSendDataDto(BaseModel):
    queue: str
    message: Dict
    correlation_id: Optional[str]
    reply_to: Optional[str]
