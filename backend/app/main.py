# app/main.py
import os
import sys

# Asegurar que el paquete 'app' pueda importarse correctamente
_base_dir = os. path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if _base_dir not in sys.path:
    sys.path.insert(0, _base_dir)

from fastapi import FastAPI, Request, status, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, StreamingResponse
from fastapi.exceptions import RequestValidationError

from app.core. config import settings
from app.api.v1.api import api_router
from app.db.base_class import Base
from app. db.session import engine
import app.models  # Asegura que los modelos estén registrados en el metadata
from app.api.v1.routers import padre_sesiones, padre_historial


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
        print("[OK] Tablas verificadas/creadas")
        
    except Exception as e:
        print(f"[WARN] Error creando tablas: {e}")


# ==================================================
# MIDDLEWARE: CORS
# ==================================================
_env = (getattr(settings, "ENVIRONMENT", "development") or "").lower()
_allow_origins = [
    "http://localhost:4200",
    "http://127.0.0.1:4200",
    "http://localhost:3240",
    "http://127.0.0.1:3240",
]
_allow_credentials = True

app.add_middleware(
    CORSMiddleware,
    allow_origins=_allow_origins,
    allow_credentials=_allow_credentials,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Nota: Evitamos añadir manualmente encabezados CORS en manejadores de excepciones
# para no interferir con CORSMiddleware. Dejar que CORSMiddleware gestione todos
# los casos (incluidos errores 401/403/500) asegura que se responda con el
# origen correcto y las credenciales según configuración.


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
            "detail":  "Error de validación en la solicitud",
            "errores":  errores,
        },
    )


# ==================================================
# INCLUIR ROUTERS V1
# ==================================================
app.include_router(
    api_router,
    prefix=settings.API_V1_PREFIX  # "/api/v1"
)

app.include_router(padre_sesiones.router, prefix="/api/v1")
app.include_router(padre_historial.router, prefix="/api/v1")


# ==================================================
# ENDPOINTS BASE
# ==================================================
@app.get("/")
def root():
    return {
        "message": settings. PROJECT_NAME,
        "version": "1.0.0",
        "docs": "/docs",
        "status": "[OK] Backend funcionando",
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

    uvicorn. run(
        "app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.RELOAD,
    )