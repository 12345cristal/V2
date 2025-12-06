# app/core/config.py

from typing import List, Optional
from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    """
    Configuración central del sistema.
    Las variables pueden ser cargadas desde un archivo .env o desde variables de entorno.
    """

    # ============================================================
    # INFORMACIÓN GENERAL
    # ============================================================
    PROJECT_NAME: str = "Autismo Mochis IA"
    API_V1_PREFIX: str = "/api/v1"

    # ============================================================
    # BASE DE DATOS (SQLAlchemy)
    # ============================================================
    DATABASE_URL: str = Field(
        default="mysql+pymysql://root:password@localhost:3306/autismo_mochis_ia",
        description="URL de conexión SQLAlchemy para MySQL"
    )

    # ============================================================
    # JWT / AUTENTICACIÓN
    # ============================================================
    JWT_SECRET_KEY: str = Field(
        ...,
        env="JWT_SECRET_KEY",
        description="Llave secreta para firmar tokens JWT"
    )
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(
        default=60 * 3,
        description="Duración del token de acceso en minutos (3 horas)"
    )

    # ============================================================
    # CORS
    # ============================================================
    BACKEND_CORS_ORIGINS: List[str] = [
        "http://localhost:4200",
        "http://127.0.0.1:4200",
    ]

    # ============================================================
    # GOOGLE GEMINI / INTELIGENCIA ARTIFICIAL
    # ============================================================
    GEMINI_API_KEY: Optional[str] = Field(
        default=None,
        env="GEMINI_API_KEY",
        description="Google Gemini API Key"
    )
    GEMINI_MODEL: str = "gemini-1.5-pro"

    # ============================================================
    # CLAVE INTERNA (microservicios)
    # ============================================================
    INTERNAL_API_KEY: str = Field(
        default="super-clave-interna",
        description="Clave interna para autenticación entre servicios"
    )

    # ============================================================
    # CONFIGURACIÓN DE Pydantic / Entorno
    # ============================================================
    class Config:
        env_file = ".env"             # Archivo de variables de entorno
        env_file_encoding = "utf-8"   # Codificación del archivo .env
        extra = "ignore"              # Ignorar variables de entorno no definidas


# Instancia global accesible desde toda la aplicación
settings = Settings()
