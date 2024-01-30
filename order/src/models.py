from sqlalchemy import Column, Integer, String, Numeric

import schemas
from app_config import settings
from db import Base


class Order(Base):
    __tablename__ = "order"
    __table_args__ = {"schema": settings.DB_SCHEMA}

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String)
    state = Column(String, default=schemas.OrderState.CREATED, server_default=f"{schemas.OrderState.CREATED}", )
    price = Column(Numeric(10, 2))
