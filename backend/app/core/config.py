# app/core/config.py
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field
from typing import List


class Settings(BaseSettings):
    # ====================================
    # GENERAL
    # ====================================
    PROJECT_NAME: str = "Autismo Mochis IA"
    API_V1_PREFIX: str = "/api/v1"

    # ====================================
    # BASE DE DATOS (MySQL)
    # ====================================
    DATABASE_URL: str = Field(
        default="mysql+pymysql://root:root@localhost:3306/autismo_mochis_ia",
        description="URL completa de conexión para SQLAlchemy"
    )

    # ====================================
    # JWT
    # ====================================
    JWT_SECRET_KEY: str = Field(..., description="Clave secreta para firmar JWT")
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 4  # 4 horas

    # ====================================
    # CORS
    # ====================================
    BACKEND_CORS_ORIGINS: List[str] = Field(
        default=["http://localhost:4200"],
        description="Orígenes permitidos para CORS"
    )

    # ====================================
    # MODELO DE CONFIGURACIÓN
    # ====================================
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

    @staticmethod
    def parse_list(value: str | List[str]) -> List[str]:
        if isinstance(value, list):
            return value
        return [item.strip() for item in value.split(",") if item.strip()]

    def __init__(self, **data):
        super().__init__(**data)
        self.BACKEND_CORS_ORIGINS = self.parse_list(self.BACKEND_CORS_ORIGINS)


settings = Settings()
