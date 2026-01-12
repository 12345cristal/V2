# app/core/config.py
from pydantic_settings import BaseSettings
from pydantic import Field, field_validator
from typing import List
import os
from pathlib import Path


class Settings(BaseSettings):
    """Configuración de la aplicación"""
    
    # Directorio base
    BASE_DIR: Path = Path(__file__).parent.parent.parent
    
    PROJECT_NAME: str = Field(default="Autismo Mochis IA")
    API_V1_PREFIX: str = Field(default="/api/v1")
    
    # Base de datos
    DB_HOST: str = Field(default="localhost")
    DB_PORT: int = Field(default=3306)
    DB_USER: str = Field(default="root")
    DB_PASSWORD: str = Field(default="root")
    DB_NAME: str = Field(default="autismo_mochis_ia")
    
    @property
    def DATABASE_URL(self) -> str:
        """Construye la URL de la base de datos"""
        return f"mysql+pymysql://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
    
    # JWT
    JWT_SECRET_KEY: str = Field(
        default="0b08b6fb2727f7c827cc9e4b60c57a166fe8eda1d2157b8d53c8803065af85c492052bb3ee301e8c708519fdce02f6929038c011c388eb20bedcee60dc2de2ea"
    )
    JWT_ALGORITHM: str = Field(default="HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(default=240)  # 4 horas
    
    # CORS
    BACKEND_CORS_ORIGINS: str = Field(default="http://localhost:4200,http://localhost:4201,http://127.0.0.1:4200,http://127.0.0.1:4201")
    
    @property
    def CORS_ORIGINS(self) -> List[str]:
        """Convierte string de CORS a lista"""
        return [origin.strip() for origin in self.BACKEND_CORS_ORIGINS.split(",")]
    
    # Servidor
    HOST: str = Field(default="0.0.0.0")
    PORT: int = Field(default=8000)
    RELOAD: bool = Field(default=True)
    
    # Ambiente
    ENVIRONMENT: str = Field(default="development")
    DEBUG: bool = Field(default=True)
    
    # API Keys y configuración de IA
    GEMINI_API_KEY: str = Field(default="")
    # Modelo Gemini 2.5 Flash (recomendado por Google para producción)
    GEMINI_MODEL: str = Field(default="gemini-2.5-flash")
    # ID de modelo (si se quiere especificar explícitamente, por defecto usa GEMINI_MODEL)
    GEMINI_MODEL_ID: str | None = Field(default=None)
    
    class Config:
        env_file = ".env"
        case_sensitive = True
        extra = "ignore"  # Ignorar campos extras del .env


# Instancia global de configuración
settings = Settings()
