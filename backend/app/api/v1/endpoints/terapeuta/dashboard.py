# app/api/v1/endpoints/terapeuta.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db

router = APIRouter(prefix="/terapeuta", tags=["Terapeuta"])

@router.get("/dashboard")
def dashboard_terapeuta(db: Session = Depends(get_db)):
    return {
        "resumen": {
            "total_ninos": 0,
            "citas_hoy": 0,
            "citas_semana": 0,
            "tareas_pendientes": 0,
            "recursos_nuevos": 0
        },
        "proximas_citas": [],
        "ninos": []
    }
