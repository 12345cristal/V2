# app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings

from app.api.v1.endpoints import auth as auth_router
from app.api.v1.endpoints import usuarios as usuarios_router
from app.api.v1.endpoints import ninos as ninos_router
from app.api.v1.endpoints import notificaciones as notificaciones_router
from app.api.v1.sockets import notifications_ws as notifications_ws_router

app = FastAPI(title=settings.PROJECT_NAME)

# ==========================
# CORS
# ==========================
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

API_PREFIX = settings.API_V1_PREFIX

# 🔐 Auth
app.include_router(auth_router.router, prefix=API_PREFIX)

# 👤 Usuarios (microservicio)
app.include_router(usuarios_router.router, prefix=API_PREFIX)

# 👶 Niños
app.include_router(ninos_router.router, prefix=API_PREFIX)

# 🔔 Notificaciones REST
app.include_router(notificaciones_router.router, prefix=API_PREFIX)

# 🔔 Notificaciones WebSocket (sin prefijo)
app.include_router(notifications_ws_router.router)


@app.get("/")
def root():
    return {"message": "Autismo Mochis IA API"}
