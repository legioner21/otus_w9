from sqlalchemy import Column, Integer, String, Numeric

from app_config import settings
from db import Base


class User(Base):
    __tablename__ = "users"
    __table_args__ = {"schema": settings.DB_SCHEMA}

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String)
    balance = Column(Numeric(10, 2))
