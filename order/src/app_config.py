from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    PROJECT_NAME: str = "otus-9-order"
    API_VSTR: str = "/api/v1"
    DATABASE_URL: str = Field(..., env="DATABASE_URL")
    DB_SCHEMA: str = Field(..., env="DB_SCHEMA")

    TASK_BROKER_URL: str = Field(..., env="TASK_BROKER_URL")
    RMQ_BILLING_IN_QUEUE_NAME: str = Field(..., env="RMQ_BILLING_IN_QUEUE_NAME")
    RMQ_BILLING_OUT_QUEUE_NAME: str = Field(..., env="RMQ_BILLING_OUT_QUEUE_NAME")
    RMQ_NOTIFY_IN_QUEUE_NAME: str = Field(..., env="RMQ_NOTIFY_IN_QUEUE_NAME")

    class Config:
        env_file = ".env"


settings = Settings()
