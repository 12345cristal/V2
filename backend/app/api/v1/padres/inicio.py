
# app/api/v1/padres/inicio.py
from fastapi import APIRouter, HTTPException
from typing import Dict, Any

router = APIRouter(
    prefix="/padres",
    tags=["Padres - Inicio"]
)

@router.get("/inicio")
def get_inicio() -> Dict[str, Any]:
    """
    Endpoint de inicio para padres.
    Retorna información básica del dashboard.
    """
    return {
        "mensaje": "Bienvenido al dashboard de padres",
        "estado": "ok"
    }

@router.get("/health")
def health_check() -> Dict[str, str]:
    """Health check del módulo de padres"""
    return {"status": "healthy", "module": "padres"}
