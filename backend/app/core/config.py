from pydantic_settings import BaseSettings
from typing import List
from pydantic import Field

class Settings(BaseSettings):
    PROJECT_NAME: str = "Autismo Mochis IA"
    API_V1_PREFIX: str = "/api/v1"

    # Base de datos (AJUSTADO A MYSQL 8)
    DATABASE_URL: str = Field(
        default="mysql+pymysql://root:root@localhost:3306/autismo_mochis_ia",
        description="SQLAlchemy database URL"
    )

    # JWT
    JWT_SECRET_KEY: str = Field(..., description="Secret key for encoding JWT")
    JWT_REFRESH_SECRET_KEY: str = Field(..., description="Secret key for refresh JWT")
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 4       # 4 horas
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7              # 7 días

    # CORS
    BACKEND_CORS_ORIGINS: List[str] = ["*"]

    class Config:
        env_file = ".env"


settings = Settings()
