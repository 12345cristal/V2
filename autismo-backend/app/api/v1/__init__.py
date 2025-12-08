"""
API v1 - Router principal
"""

from fastapi import APIRouter
from app.api.v1.endpoints import auth

api_router = APIRouter()

# Registrar routers de endpoints
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])

# TODO: Agregar más routers conforme se implementen
# api_router.include_router(usuarios.router, prefix="/usuarios", tags=["usuarios"])
# api_router.include_router(roles.router, prefix="/roles", tags=["roles"])
# api_router.include_router(personal.router, prefix="/personal", tags=["personal"])
# api_router.include_router(tutores.router, prefix="/tutores", tags=["tutores"])
# api_router.include_router(ninos.router, prefix="/ninos", tags=["ninos"])
# api_router.include_router(terapias.router, prefix="/terapias", tags=["terapias"])
# api_router.include_router(citas.router, prefix="/citas", tags=["citas"])
# api_router.include_router(sesiones.router, prefix="/sesiones", tags=["sesiones"])
# api_router.include_router(recursos.router, prefix="/recursos", tags=["recursos"])
# api_router.include_router(notificaciones.router, prefix="/notificaciones", tags=["notificaciones"])
# api_router.include_router(priorizacion.router, prefix="/priorizacion", tags=["priorizacion"])
# api_router.include_router(ia.router, prefix="/ia", tags=["ia"])
