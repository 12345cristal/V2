# app/core/config.py

from pydantic_settings import BaseSettings
from pydantic import Field
from typing import Optional


class Settings(BaseSettings):
    # =====================================================
    # INFORMACIÓN GENERAL DEL PROYECTO
    # =====================================================
    PROJECT_NAME: str = "Autismo Mochis IA"
    API_V1_PREFIX: str = "/api/v1"

    # =====================================================
    # BASE DE DATOS
    # =====================================================
    DATABASE_URL: str = Field(..., env="DATABASE_URL")

    # =====================================================
    # JWT / AUTENTICACIÓN
    # =====================================================
    JWT_SECRET_KEY: str = Field(..., env="JWT_SECRET_KEY")
    JWT_ALGORITHM: str = Field(default="HS256", env="JWT_ALGORITHM")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(default=240, env="ACCESS_TOKEN_EXPIRE_MINUTES")

    # =====================================================
    # CORS
    # =====================================================
    BACKEND_CORS_ORIGINS: list[str] = ["*"]

    # =====================================================
    # GEMINI / GOOGLE AI
    # =====================================================
    GEMINI_API_KEY: Optional[str] = Field(default=None, env="GEMINI_API_KEY")
    GEMINI_MODEL_ID: str = Field(default="models/gemini-2.5-flash", env="GEMINI_MODEL_ID")
    GEMINI_TIMEOUT_MS: int = Field(default=120000, env="GEMINI_TIMEOUT_MS")

    class Config:
        env_file = ".env"
        case_sensitive = True


# Instancia global
settings = Settings()
