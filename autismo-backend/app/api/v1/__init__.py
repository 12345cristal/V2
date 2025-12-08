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

# Registrar routers de endpoints
api_router.include_router(auth.router, prefix="/auth", tags=["Autenticación"])
api_router.include_router(usuarios.router, tags=["Usuarios"])
api_router.include_router(roles.router, tags=["Roles y Permisos"])
api_router.include_router(personal.router, tags=["Personal (Terapeutas)"])
api_router.include_router(tutores.router, tags=["Tutores (Padres)"])
api_router.include_router(ninos.router, tags=["Niños (Beneficiados)"])
api_router.include_router(terapias.router, tags=["Terapias y Sesiones"])
api_router.include_router(citas.router, tags=["Citas y Programación"])
api_router.include_router(recursos.router, tags=["Recursos Educativos"])
api_router.include_router(notificaciones.router, tags=["Notificaciones"])
api_router.include_router(priorizacion.router, tags=["Priorización (TOPSIS)"])
api_router.include_router(ia.router, tags=["IA (Gemini)"])
api_router.include_router(coordinador_dashboard.router)

# TODO: Agregar más routers conforme se implementen
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
