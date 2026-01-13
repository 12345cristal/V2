# app/core/config.py
from pydantic_settings import BaseSettings
from typing import List
from pathlib import Path

# ==================================================
# DIRECTORIO BASE DEL PROYECTO
# ==================================================
BASE_DIR = Path(__file__).resolve().parent.parent.parent


class Settings(BaseSettings):
    # ==================================================
    # PROYECTO
    # ==================================================
    PROJECT_NAME: str = "Autismo Mochis IA"
    PROJECT_VERSION: str = "2.0.0"
    DESCRIPTION: str = "Backend para sistema de apoyo terapéutico TEA"

    # ==================================================
    # DIRECTORIOS
    # ==================================================
    BASE_DIR: Path = BASE_DIR
    UPLOADS_DIR: Path = BASE_DIR / "uploads"

    # ==================================================
    # API
    # ==================================================
    API_V1_PREFIX: str = "/api/v1"

    # ==================================================
    # BASE DE DATOS (MySQL)
    # ==================================================
    DB_HOST: str = "localhost"
    DB_PORT: int = 3306
    DB_USER: str = "root"
    DB_PASSWORD: str = "root"
    DB_NAME: str = "autismo_mochis_ia"
    SQLALCHEMY_ECHO: bool = False

    @property
    def DATABASE_URL(self) -> str:
        """
        URL de conexión SQLAlchemy
        """
        return (
            f"mysql+pymysql://{self.DB_USER}:"
            f"{self.DB_PASSWORD}@"
            f"{self.DB_HOST}:{self.DB_PORT}/"
            f"{self.DB_NAME}"
        )

    # ==================================================
    # JWT / AUTENTICACIÓN
    # ==================================================
    JWT_SECRET_KEY: str = (
        "0b08b6fb2727f7c827cc9e4b60c57a166fe8eda1d2157b8d53c8803"
        "065af85c492052bb3ee301e8c708519fdce02f6929038c011c388"
        "eb20bedcee60dc2de2ea"
    )
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 240

    # ==================================================
    # CORS
    # ==================================================
    # Se define como string para .env y se parsea a lista
    BACKEND_CORS_ORIGINS: str = (
        "http://localhost:4200,"
        "http://127.0.0.1:4200"
    )

    @property
    def CORS_ORIGINS(self) -> List[str]:
        """
        Convierte BACKEND_CORS_ORIGINS en lista limpia
        """
        return [
            origin.strip()
            for origin in self.BACKEND_CORS_ORIGINS.split(",")
            if origin.strip()
        ]

    # ==================================================
    # SERVIDOR
    # ==================================================
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    RELOAD: bool = True

    # ==================================================
    # ENTORNO
    # ==================================================
    ENVIRONMENT: str = "development"
    DEBUG: bool = True

    # ==================================================
    # GEMINI / IA
    # ==================================================
    GEMINI_API_KEY: str = ""
    GEMINI_MODEL: str = "gemini-2.5-flash"

    # ==================================================
    # CONFIGURACIÓN Pydantic
    # ==================================================
    class Config:
        env_file = ".env"
        case_sensitive = True
        extra = "allow"


# ==================================================
# INSTANCIA GLOBAL
# ==================================================
settings = Settings()
