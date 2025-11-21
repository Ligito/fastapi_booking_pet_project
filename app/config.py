from pydantic_settings import BaseSettings
from pydantic import computed_field



class Settings(BaseSettings):
    DB_HOST:str
    DB_PORT:int
    DB_USER:str
    DB_PASS:str
    DB_NAME:str
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

    @computed_field
    @property
    def DATABASE_URL(self) -> str:
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    class Config:
        env_file = ".env"

settings = Settings()


