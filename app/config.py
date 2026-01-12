from typing import Literal

from pydantic import ConfigDict, computed_field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    MODE:Literal["DEV", "TEST", "PROD"]
    LOG_LEVEL:Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]

    DB_HOST:str
    DB_PORT:int
    DB_USER:str
    DB_PASS:str
    DB_NAME:str

    TEST_DB_HOST:str
    TEST_DB_PORT:int
    TEST_DB_USER:str
    TEST_DB_PASS:str
    TEST_DB_NAME:str

    SECRET_KEY:str
    ALGORITHM:str

    REDIS_HOST:str
    REDIS_PORT:int

    SMTP_HOST:str
    SMTP_PORT:int
    SMTP_USER:str
    SMTP_PASS:str

    TELEGRAM_BOT_TOKEN:str
    # CHAT_ID захардкожен на мой что бы не обновлять БС(возможная доработка)
    TELEGRAM_BOT_CHAT_ID:int

    model_config = ConfigDict(env_file=".env")

    @computed_field
    @property
    def DATABASE_URL(self) -> str:
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    @computed_field
    @property
    def TEST_DATABASE_URL(self) -> str:
        return f"postgresql+asyncpg://{self.TEST_DB_USER}:{self.TEST_DB_PASS}@{self.TEST_DB_HOST}:{self.TEST_DB_PORT}/{self.TEST_DB_NAME}"

    # class Config:
    #     env_file = ".env"

settings = Settings()


