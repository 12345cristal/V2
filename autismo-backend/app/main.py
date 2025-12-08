# app/main.py
"""
Autismo Mochis IA - Backend API
FastAPI + SQLAlchemy + MySQL
"""

from fastapi import FastAPI, Request, status, WebSocket, WebSocketDisconnect
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
    redirect_slashes=False,  # Evitar redirecciones que causan problemas de CORS
)

# =====================================================
# MIDDLEWARE: CORS
# =====================================================

# CORS: En desarrollo permitir todos los orígenes
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],            # En desarrollo: permitir todos
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
# WEBSOCKET: NOTIFICACIONES EN TIEMPO REAL
# =====================================================

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """
    WebSocket para notificaciones en tiempo real.
    Acepta conexiones desde Angular con token JWT.
    """
    # Verificar origen
    origin = websocket.headers.get("origin")
    allowed_origins = ["http://localhost:4200", "http://127.0.0.1:4200"]
    
    if origin not in allowed_origins and origin is not None:
        await websocket.close(code=1008)  # Policy violation
        return
    
    # Aceptar conexión
    await websocket.accept()
    
    try:
        # Obtener token del query param
        token = websocket.query_params.get("token")
        
        if not token:
            await websocket.send_json({"error": "Token requerido"})
            await websocket.close()
            return
        
        # Aquí puedes validar el token JWT si lo necesitas
        # user = await verify_token(token)
        
        # Mantener conexión abierta y enviar mensajes
        await websocket.send_json({
            "type": "connection",
            "message": "Conectado al servidor de notificaciones"
        })
        
        # Loop para recibir mensajes
        while True:
            data = await websocket.receive_text()
            # Aquí puedes procesar mensajes del cliente
            await websocket.send_json({
                "type": "echo",
                "message": f"Recibido: {data}"
            })
            
    except WebSocketDisconnect:
        print("Cliente desconectado del WebSocket")
    except Exception as e:
        print(f"Error en WebSocket: {e}")
        await websocket.close()


# =====================================================
# EVENTOS STARTUP / SHUTDOWN
# =====================================================

@app.on_event("startup")
async def startup_event():
    """Eventos al iniciar la aplicación"""
    print(f">> Iniciando {settings.PROJECT_NAME}")
    print(">> Documentacion disponible en: /api/docs")


@app.on_event("shutdown")
async def shutdown_event():
    """Eventos al cerrar la aplicación"""
    print(f">> Cerrando {settings.PROJECT_NAME}")
