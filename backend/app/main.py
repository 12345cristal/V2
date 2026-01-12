# app/main.py
import os
import sys
from datetime import datetime
from pathlib import Path

# Asegurar que el paquete 'app' pueda importarse correctamente
_base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if _base_dir not in sys.path:
    sys.path.insert(0, _base_dir)

from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from fastapi.staticfiles import StaticFiles

from app.core.config import settings
from app.api.v1.api import api_router
from app.db.base_class import Base
from app.db.session import engine
import app.models  # Asegura que los modelos estén registrados en el metadata
from app.api.v1.routers import (
    notificaciones,
    recursos,
    tareas_recurso,
    planes_pago,
    pagos,
    ninos,
    terapias_nino
)


# ==================================================
# CREAR APLICACIÓN FASTAPI
# ==================================================
app = FastAPI(
    title="Sistema Autismo Mochis IA",
    description="API para el sistema de gestión de terapias con integración a BD MySQL autismo_mochis_ia",
    version="2.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
)

# Crear tablas automáticamente si no existen
@app.on_event("startup")
def on_startup():
    """Inicialización al arrancar la aplicación"""
    try:
        Base.metadata.create_all(bind=engine)
        print("[✓] Tablas verificadas/creadas en la base de datos")
        
        # Crear directorios para archivos si no existen
        Path("uploads/tareas_recurso/evidencias").mkdir(parents=True, exist_ok=True)
        print("[✓] Directorios de uploads creados")
        
    except Exception as e:
        print(f"[!] Error en inicialización: {e}")


# ==================================================
# MIDDLEWARE: CORS
# ==================================================
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ==================================================
# MANEJADOR GLOBAL DE ERRORES DE VALIDACIÓN
# ==================================================
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
    request: Request,
    exc: RequestValidationError
):
    """Respuesta amigable para errores de validación"""
    print(f"❌ Error de validación en {request.url}")
    
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
            "detail": "Error de validación en la solicitud",
            "errores": errores,
        },
    )


# ==================================================
# INCLUIR ROUTERS V1
# ==================================================
app.include_router(
    api_router,
    prefix=settings.API_V1_PREFIX  # "/api/v1"
)

# Routers de nueva estructura BD real
app.include_router(notificaciones.router, prefix="/api/v1")
app.include_router(recursos.router, prefix="/api/v1")
app.include_router(tareas_recurso.router, prefix="/api/v1")
app.include_router(planes_pago.router, prefix="/api/v1")
app.include_router(pagos.router, prefix="/api/v1")
app.include_router(ninos.router, prefix="/api/v1")
app.include_router(terapias_nino.router, prefix="/api/v1")


# ==================================================
# MONTAJE DE ARCHIVOS ESTÁTICOS
# ==================================================
try:
    app.mount("/archivos/tareas_recurso", StaticFiles(directory="uploads/tareas_recurso"), name="tareas_recurso_archivos")
    print("[✓] Archivos estáticos montados correctamente")
except RuntimeError as e:
    print(f"[!] Advertencia: No se pudo montar directorio de uploads: {e}")
    print("[i] Los directorios se crearán automáticamente en el startup")
except Exception as e:
    print(f"[!] Error inesperado montando archivos estáticos: {e}")
    import traceback
    traceback.print_exc()


# ==================================================
# ENDPOINTS BASE
# ==================================================
@app.get("/")
def root():
    """Endpoint raíz con información del sistema"""
    return {
        "message": "API Sistema Autismo Mochis IA",
        "version": "2.0.0",
        "database": settings.DB_NAME,
        "timestamp": datetime.now().isoformat(),
        "status": "operational"
    }


@app.get("/ping")
def ping():
    """Endpoint de verificación rápida"""
    return {
        "status": "[OK] Backend funcionando",
        "docs": "/docs"
    }


@app.get("/health")
def health_check():
    """Endpoint de verificación de salud del servicio"""
    return {
        "status": "healthy",
        "service": settings.PROJECT_NAME,
        "database": settings.DB_NAME
    }


# ==================================================
# EJECUCIÓN LOCAL
# ==================================================
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.RELOAD,
    )