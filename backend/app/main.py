# app/main.py
from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError

from slowapi.errors import RateLimitExceeded
from slowapi import Limiter
from slowapi.util import get_remote_address

from app.core.config import settings
from app.api.v1.api import api_router
from app.core.rate_limit import limiter


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

# Añadir limiter al estado de la app
app.state.limiter = limiter


# ==================================================
# MIDDLEWARE: RATE LIMIT
# ==================================================
@app.exception_handler(RateLimitExceeded)
async def rate_limit_handler(request: Request, exc: RateLimitExceeded):
    """Manejador personalizado para rate limit"""
    return JSONResponse(
        status_code=429,
        content={"detail": "Demasiadas solicitudes. Intenta de nuevo en unos segundos."}
    )


# ==================================================
# MIDDLEWARE: CORS
# ==================================================
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS if hasattr(settings, 'CORS_ORIGINS') else ["http://localhost:4200"],
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
        "status": "✅ Backend funcionando"
    }

@app.get("/")
def root():
    return {
        "message": "API Autismo Mochis IA",
        "version": "1.0.0",
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
