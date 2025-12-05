from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.core.security import JWTBearer
from app.db.session import engine
from app.db import base  # importa los modelos
from app.utils.audit_middleware import audit_middleware

def create_application() -> FastAPI:
    app = FastAPI(
        title=settings.PROJECT_NAME,
        version="1.0.0",
        description="Backend Autismo Mochis IA"
    )

    # CORS para Angular
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.BACKEND_CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Middleware de Auditoría
    app.middleware("http")(audit_middleware)

    # Aquí se montarán los routers de cada módulo
    # app.include_router(auth_router, prefix=settings.API_V1_PREFIX)
    # app.include_router(usuarios_router, prefix=settings.API_V1_PREFIX)
    # app.include_router(ninos_router, prefix=settings.API_V1_PREFIX)
    # ...

    return app


app = create_application()
