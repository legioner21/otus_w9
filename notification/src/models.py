from sqlalchemy import Column, Integer, String, Numeric

from app_config import settings
from db import Base


class Notification(Base):
    __tablename__ = "notification"
    __table_args__ = {"schema": settings.DB_SCHEMA}

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer)
    order_id = Column(Integer)
    text = Column(String)
