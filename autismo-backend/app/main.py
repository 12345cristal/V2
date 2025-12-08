# app/main.py
"""
Autismo Mochis IA - Backend API
FastAPI + SQLAlchemy + MySQL
"""

from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from sqlalchemy.exc import SQLAlchemyError

from app.core.config import settings
from app.api.v1 import api_router

# =====================================================
# CREAR APP FastAPI
# =====================================================

app = FastAPI(
    title=settings.PROJECT_NAME,
    version="1.0.0",
    description="API para sistema de gestión de terapias para niños con autismo",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
)

# =====================================================
# MIDDLEWARE: CORS
# =====================================================

# En desarrollo: permitimos específicamente Angular local
origins = [
    "http://localhost:4200",
    "http://127.0.0.1:4200",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,          # evitar "*", mejor dominios concretos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)

# =====================================================
# MANEJO DE ERRORES GLOBAL
# =====================================================

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """
    Manejo de errores de validación de Pydantic
    """
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "detail": "Error de validación",
            "errors": exc.errors(),
        },
    )


@app.exception_handler(SQLAlchemyError)
async def sqlalchemy_exception_handler(request: Request, exc: SQLAlchemyError):
    """
    Manejo de errores de base de datos
    """
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "detail": "Error en la base de datos",
            "error": str(exc) if settings.DEBUG else "Internal server error",
        },
    )


# =====================================================
# RUTAS BÁSICAS
# =====================================================

@app.get("/")
def root():
    """Health check endpoint"""
    return {
        "message": f"{settings.PROJECT_NAME} API",
        "version": "1.0.0",
        "status": "running",
    }


@app.get("/health")
def health_check():
    """Endpoint de salud para monitoreo"""
    return {"status": "healthy"}


# Incluir router principal de API v1
app.include_router(api_router, prefix=settings.API_V1_PREFIX)


# =====================================================
# EVENTOS STARTUP / SHUTDOWN
# =====================================================

@app.on_event("startup")
async def startup_event():
    """Eventos al iniciar la aplicación"""
    print(f"Iniciando {settings.PROJECT_NAME}")
    print("Documentación disponible en: /api/docs")


@app.on_event("shutdown")
async def shutdown_event():
    """Eventos al cerrar la aplicación"""
    print(f"Cerrando {settings.PROJECT_NAME}")
