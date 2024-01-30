from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    PROJECT_NAME: str = "otus-9-billing"
    API_VSTR: str = "/api/v1"
    DATABASE_URL: str = Field(..., env="DATABASE_URL")
    DB_SCHEMA: str = Field(..., env="DB_SCHEMA")

    TASK_BROKER_URL: str = Field(..., env="TASK_BROKER_URL")
    RMQ_ORDER_IN_QUEUE_NAME: str = Field(..., env="RMQ_ORDER_IN_QUEUE_NAME")

    class Config:
        env_file = ".env"


settings = Settings()
