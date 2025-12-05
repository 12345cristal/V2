# app/core/config.py
from pydantic_settings import BaseSettings
from pydantic import Field
from typing import List


class Settings(BaseSettings):
    PROJECT_NAME: str = "Autismo Mochis IA"
    API_V1_PREFIX: str = "/api/v1"

    # BD: ajusta a tu usuario / password reales
    DATABASE_URL: str = Field(
        default="mysql+pymysql://root:password@localhost:3306/autismo_mochis_ia",
        description="SQLAlchemy database URL"
    )

    # JWT (3 horas)
    JWT_SECRET_KEY: str = Field(..., env="JWT_SECRET_KEY")
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 3  # 3 horas

    # CORS
    BACKEND_CORS_ORIGINS: List[str] = ["http://localhost:4200"]

    # IA / GEMINI
    GEMINI_API_KEY: str | None = Field(default=None, env="GEMINI_API_KEY")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
