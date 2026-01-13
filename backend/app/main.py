# app/main.py
from datetime import datetime
from pathlib import Path
import logging

from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from fastapi.staticfiles import StaticFiles

from app.core.config import settings
from app.api.v1.api import api_router
from app.db.session import init_db

# ==================================================
# CREAR APLICACIÓN FASTAPI
# ==================================================
app = FastAPI(
    title=settings.PROJECT_NAME,
    description="API Sistema Autismo Mochis IA",
    version="2.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
)

logging.basicConfig(level=logging.INFO)

# ==================================================
# STARTUP
# ==================================================
@app.on_event("startup")
def on_startup():
    init_db()

    # Crear directorios necesarios
    Path("uploads/tareas_recurso/evidencias").mkdir(parents=True, exist_ok=True)
    logging.info("✓ Base de datos y directorios inicializados")

# ==================================================
# CORS
# ==================================================
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==================================================
# MANEJO GLOBAL DE ERRORES
# ==================================================
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
    request: Request,
    exc: RequestValidationError
):
    errores = [
        {
            "campo": " -> ".join(map(str, e["loc"])),
            "mensaje": e["msg"],
            "tipo": e["type"],
        }
        for e in exc.errors()
    ]

    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={
            "detail": "Error de validación",
            "errores": errores,
        },
    )

# ==================================================
# ROUTERS
# ==================================================
app.include_router(api_router, prefix=settings.API_V1_PREFIX)

# ==================================================
# ARCHIVOS ESTÁTICOS
# ==================================================
app.mount(
    "/archivos",
    StaticFiles(directory="uploads"),
    name="archivos",
)

# ==================================================
# ENDPOINTS BASE
# ==================================================
@app.get("/")
def root():
    return {
        "message": "API Autismo Mochis IA",
        "version": "2.0.0",
        "database": settings.DB_NAME,
        "timestamp": datetime.now().isoformat(),
        "status": "operational",
    }


@app.get("/ping")
def ping():
    return {"status": "OK", "docs": "/docs"}
