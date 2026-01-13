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
# CONFIGURACIÓN LOGGING
# ==================================================
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

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

# ==================================================
# CORS (⚠️ DEBE IR ANTES DE LOS ROUTERS)
# ==================================================
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==================================================
# STARTUP
# ==================================================
@app.on_event("startup")
def on_startup():
    # Inicializar BD
    init_db()

    # Crear directorios necesarios
    Path("uploads").mkdir(exist_ok=True)
    Path("uploads/tareas_recurso").mkdir(parents=True, exist_ok=True)
    Path("uploads/tareas_recurso/evidencias").mkdir(parents=True, exist_ok=True)

    logging.info("✓ Base de datos inicializada")
    logging.info("✓ Directorios de uploads verificados")

# ==================================================
# MANEJO GLOBAL DE ERRORES DE VALIDACIÓN
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
# ROUTERS API V1
# ==================================================
app.include_router(
    api_router,
    prefix=settings.API_V1_PREFIX
)

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
@app.get("/", tags=["Root"])
def root():
    return {
        "message": "API Autismo Mochis IA",
        "version": "2.0.0",
        "database": settings.DB_NAME,
        "timestamp": datetime.now().isoformat(),
        "status": "operational",
    }


@app.get("/ping", tags=["Health"])
def ping():
    return {
        "status": "OK",
        "docs": "/docs",
        "api": settings.API_V1_PREFIX
    }
