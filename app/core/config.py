from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):

    DATABASE_URL: str

    APP_NAME: str = "Auction Service"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False

    BACKEND_CORS_ORIGINS: list[str] = ["*"]
    
    class Config:
        env_file = ".env.dist"
        case_sensitive = True


settings = Settings()