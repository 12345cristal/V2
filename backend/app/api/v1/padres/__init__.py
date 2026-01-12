# app/api/v1/padres/__init__.py
from fastapi import APIRouter

from .inicio import router as inicio_router
from .mis_hijos import router as mis_hijos_router

# Combinar routers
padres_router = APIRouter()
padres_router.include_router(inicio_router)
padres_router.include_router(mis_hijos_router)

__all__ = ["padres_router"]
