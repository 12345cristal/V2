from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "Autismo IA Service"
    GEMINI_API_KEY: str
    # Clave interna para llamadas entre servicios
    INTERNAL_API_KEY: str = "super-clave-interna"

    class Config:
        env_file = ".env"


settings = Settings()
