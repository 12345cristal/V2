# app/api/v1/endpoints/padre/router.py
"""
Router principal del módulo Padre
Combina todos los sub-routers del módulo
"""
from fastapi import APIRouter
from app.api.v1.endpoints.padre import (
    dashboard,
    mis_hijos,
    sesiones,
    historial,
    tareas,
    pagos,
    documentos,
    recursos,
    mensajes,
    notificaciones,
    perfil_padre
)


router = APIRouter()

# Dashboard
router.include_router(dashboard.router, tags=["Padre - Dashboard"])

# Mis Hijos
router.include_router(mis_hijos.router, tags=["Padre - Hijos"])

# Sesiones
router.include_router(sesiones.router, tags=["Padre - Sesiones"])

# Historial Terapéutico
router.include_router(historial.router, tags=["Padre - Historial"])

# Tareas
router.include_router(tareas.router, tags=["Padre - Tareas"])

# Pagos
router.include_router(pagos.router, tags=["Padre - Pagos"])

# Documentos
router.include_router(documentos.router, tags=["Padre - Documentos"])

# Recursos Recomendados
router.include_router(recursos.router, tags=["Padre - Recursos"])

# Mensajes
router.include_router(mensajes.router, tags=["Padre - Mensajes"])

# Notificaciones
router.include_router(notificaciones.router, tags=["Padre - Notificaciones"])

# Perfil y Accesibilidad
router.include_router(perfil_padre.router, tags=["Padre - Perfil"])
