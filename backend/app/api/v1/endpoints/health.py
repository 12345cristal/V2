"""
Endpoint de salud
"""
from fastapi import APIRouter

router = APIRouter()

@router.get("/health")
def health():
    """
    Health check del servidor
    """
    return {"status": "ok", "message": "Backend funcionando correctamente"}
