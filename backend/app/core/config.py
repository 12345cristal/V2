# app/core/config.py

from pydantic_settings import BaseSettings
from pydantic import Field
from typing import List, Optional


class Settings(BaseSettings):
    # ========================================
    # INFORMACIÓN GENERAL
    # ========================================
    PROJECT_NAME: str = "Autismo Mochis IA"
    API_V1_PREFIX: str = "/api/v1"

    # ========================================
    # BASE DE DATOS
    # ========================================
    DATABASE_URL: str = Field(
        default="mysql+pymysql://root:password@localhost:3306/autismo_mochis_ia",
        description="SQLAlchemy database URL"
    )

    # ========================================
    # JWT
    # ========================================
    JWT_SECRET_KEY: str = Field(..., env="JWT_SECRET_KEY")
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 3  # 3 horas

    # ========================================
    # CORS
    # ========================================
    BACKEND_CORS_ORIGINS: List[str] = [
        "http://localhost:4200",
        "http://127.0.0.1:4200",
    ]

    # ========================================
    # GOOGLE GEMINI / IA
    # ========================================
    GEMINI_API_KEY: Optional[str] = Field(
        default=None,
        env="GEMINI_API_KEY",
        description="Google Gemini API Key"
    )

    GEMINI_MODEL: str = "gemini-1.5-pro"

    # ========================================
    # CONFIG GLOBAL
    # ========================================
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
