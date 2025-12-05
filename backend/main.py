# app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import get_settings
from app.api.v1.endpoints import auth as auth_router

settings = get_settings()


def create_application() -> FastAPI:
    app = FastAPI(
        title=settings.PROJECT_NAME,
        version="1.0.0",
    )

    # ======================
    # CORS
    # ======================
    if settings.BACKEND_CORS_ORIGINS:
        app.add_middleware(
            CORSMiddleware,
            allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

    # ======================
    # ROUTERS V1
    # ======================
    app.include_router(auth_router.router, prefix=settings.API_V1_PREFIX)

    @app.get("/")
    def root():
        return {"detail": "Autismo Mochis IA API - OK"}

    return app


app = create_application()
