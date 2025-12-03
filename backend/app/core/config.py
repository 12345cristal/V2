# app/core/config.py
from pydantic_settings import BaseSettings
from pydantic import AnyUrl, Field
from typing import List


class Settings(BaseSettings):
    PROJECT_NAME: str = "Autismo Mochis IA"
    API_V1_PREFIX: str = "/api/v1"

    # BD: ajusta para MySQL
    DATABASE_URL: str = Field(
        default="mysql+pymysql://user:root@localhost:3306/autismo_mochis_ia",
        description="SQLAlchemy database URL"
    )

    # JWT
    JWT_SECRET_KEY: str = "cambia-esto-por-uno-muy-largo-y-seguro"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 4  # 4 horas

    # CORS
    BACKEND_CORS_ORIGINS: List[str] = ["http://localhost:4200"]

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
