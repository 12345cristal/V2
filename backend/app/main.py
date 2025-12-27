# app/main.py
import os
import sys

# Asegurar que el paquete 'app' pueda importarse correctamente
_base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if _base_dir not in sys.path:
    sys.path.insert(0, _base_dir)

from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError

from app.core.config import settings
from app.api.v1.api import api_router
from app.db.base import Base
from app.db.session import engine


# ==================================================
# CREAR APLICACIÓN FASTAPI
# ==================================================
app = FastAPI(
    title=settings.PROJECT_NAME,
    description="API para el sistema de gestión de centro de atención de autismo con IA",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
)

# Crear tablas automáticamente si no existen (evita 1146)
@app.on_event("startup")
def on_startup():
    try:
        Base.metadata.create_all(bind=engine)
        print("[OK] Tablas de chat verificadas/creadas")
    except Exception as e:
        print(f"[WARN] Error creando tablas: {e}")


# ==================================================
# MIDDLEWARE: CORS
# ==================================================
_env = (getattr(settings, "ENVIRONMENT", "development") or "").lower()
_allow_origins = settings.CORS_ORIGINS if hasattr(settings, 'CORS_ORIGINS') else ["http://localhost:4200"]
_allow_credentials = True

if _env == "development":
    _allow_origins = ["*"]
    _allow_credentials = False

app.add_middleware(
    CORSMiddleware,
    allow_origins=_allow_origins,
    allow_credentials=_allow_credentials,
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
    """Respuesta amable para errores de validación"""
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


# ==================================================
# ENDPOINTS BASE
# ==================================================
@app.get("/")
def root():
    return {
        "message": settings.PROJECT_NAME,
        "version": "1.0.0",
        "docs": "/docs",
        "status": "[OK] Backend funcionando"
    }

@app.get("/ping")
def ping():
    return {
        "status": "running",
        "docs": "/docs",
    }


@app.get("/health")
def health():
    return {
        "status": "healthy",
        "service": settings.PROJECT_NAME,
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
