# app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.api.v1.endpoints import auth, usuarios
from app.api.v1.sockets import chat_ws, notifications_ws


def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.PROJECT_NAME,
        openapi_url=f"{settings.API_V1_PREFIX}/openapi.json",
    )

    # CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.BACKEND_CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # API HTTP
    app.include_router(
        auth.router,
        prefix=settings.API_V1_PREFIX,
    )
    app.include_router(
        usuarios.router,
        prefix=settings.API_V1_PREFIX,
    )

    # WebSockets
    app.include_router(chat_ws.router)
    app.include_router(notifications_ws.router)

    return app


app = create_app()
