# app/core/config.py
from functools import lru_cache
from typing import List, Optional

from pydantic_settings import BaseSettings
from pydantic import AnyHttpUrl, field_validator


class Settings(BaseSettings):
    PROJECT_NAME: str = "Autismo Mochis IA"
    API_V1_PREFIX: str = "/api/v1"

    # BD MySQL (ajusta user/pass/host/puerto)
    DATABASE_URL: str = (
        "mysql+pymysql://root:root@localhost:3306/autismo_mochis_ia"
    )

    # JWT
    JWT_SECRET_KEY: str = (
        "super-secret-key-change-me"  # cámbiala en .env
    )
    JWT_REFRESH_SECRET_KEY: str = (
        "super-refresh-secret-key-change-me"  # cámbiala en .env
    )
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 4   # 4 horas
    REFRESH_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 días

    # CORS
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] | List[str] = ["*"]

    @field_validator("BACKEND_CORS_ORIGINS", mode="before")
    @classmethod
    def assemble_cors_origins(cls, v):
        if isinstance(v, str) and not v.startswith("["):
            # Separa por comas si viene de env tipo: "http://localhost,http://otro"
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, tuple)):
            return v
        return v

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


@lru_cache
def get_settings() -> Settings:
    return Settings()
