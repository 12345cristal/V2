# app/api/v1/__init__.py
"""
API v1 - Router principal
"""

from fastapi import APIRouter

from app.api.v1.endpoints import (
    auth,
    usuarios,
    roles,
    personal,
    tutores,
    ninos,
    terapias,
    citas,
    recursos,
    notificaciones,
    priorizacion,
    ia,
    coordinador_dashboard,
)

api_router = APIRouter()

# ============================
# Registrar routers de endpoints
# ============================

api_router.include_router(auth.router, prefix="/auth", tags=["Autenticación"])
api_router.include_router(usuarios.router, prefix="/usuarios", tags=["Usuarios"])
api_router.include_router(roles.router, prefix="/roles", tags=["Roles y Permisos"])
api_router.include_router(
    personal.router, prefix="/personal", tags=["Personal (Terapeutas)"]
)
api_router.include_router(
    tutores.router, prefix="/tutores", tags=["Tutores (Padres)"]
)
api_router.include_router(
    ninos.router, prefix="/ninos", tags=["Niños (Beneficiados)"]
)
api_router.include_router(
    terapias.router, prefix="/terapias", tags=["Terapias y Sesiones"]
)
api_router.include_router(
    citas.router, prefix="/citas", tags=["Citas y Programación"]
)
api_router.include_router(
    recursos.router, prefix="/recursos", tags=["Recursos Educativos"]
)
api_router.include_router(
    notificaciones.router, prefix="/notificaciones", tags=["Notificaciones"]
)
api_router.include_router(
    priorizacion.router, prefix="/priorizacion", tags=["Priorización (TOPSIS)"]
)
api_router.include_router(ia.router, prefix="/ia", tags=["IA (Gemini)"])

# Dashboard coordinador (ya tiene prefix="/coordinador" en el router)
api_router.include_router(coordinador_dashboard.router)
