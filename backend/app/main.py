# app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api.v1 import api_router


# ==================================================
# CREAR APLICACIÓN FASTAPI
# ==================================================
app = FastAPI(
    title=settings.PROJECT_NAME,
    description="API para el sistema de gestión de centro de atención de autismo",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)


# ==================================================
# MIDDLEWARE CORS
# ==================================================
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ==================================================
# INCLUIR ROUTERS
# ==================================================
app.include_router(api_router, prefix=settings.API_V1_PREFIX)


# ==================================================
# ENDPOINTS PRINCIPALES
# ==================================================
@app.get("/")
def root():
    """Endpoint raíz"""
    return {
        "message": "API Autismo Mochis IA",
        "version": "1.0.0",
        "status": "running",
        "docs": "/docs"
    }


@app.get("/health")
def health_check():
    """Endpoint de health check"""
    return {
        "status": "healthy",
        "service": settings.PROJECT_NAME
    }


# ==================================================
# EJECUCIÓN CON UVICORN
# ==================================================
if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.RELOAD
    )
