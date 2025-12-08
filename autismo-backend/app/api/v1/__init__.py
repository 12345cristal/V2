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
api_router.include_router(personal.router, prefix="/personal", tags=["Personal"])
api_router.include_router(tutores.router, prefix="/tutores", tags=["Tutores"])

# ⬅️ IMPORTANTE: ESTE YA TIENE prefix="/ninos" ADENTRO
api_router.include_router(ninos.router)

api_router.include_router(terapias.router, prefix="/terapias", tags=["Terapias"])
api_router.include_router(citas.router, prefix="/citas", tags=["Citas"])
api_router.include_router(recursos.router, prefix="/recursos", tags=["Recursos"])
api_router.include_router(notificaciones.router, prefix="/notificaciones", tags=["Notificaciones"])
api_router.include_router(priorizacion.router, prefix="/priorizacion", tags=["TOPSIS"])
api_router.include_router(ia.router, prefix="/ia", tags=["IA"])

# Ya trae su propio prefix="/coordinador"
api_router.include_router(coordinador_dashboard.router)
