from fastapi import APIRouter
from pydantic import BaseModel
from typing import List

from app.services.topsis_service import TopsisService

router = APIRouter(prefix="/topsis")


class TopsisRequest(BaseModel):
    matriz: List[List[float]]
    pesos: List[float]
    tipos: List[str]  # 'beneficio' o 'costo' (si quieres usarla)


@router.post("/actividades")
def topsis_actividades(payload: TopsisRequest):
    """
    POST /topsis/actividades
    Body:
    {
      "matriz": [[...],[...]],
      "pesos": [...],
      "tipos": ["beneficio", "costo", ...]
    }
    """
    return TopsisService.evaluar(payload.matriz, payload.pesos, payload.tipos)


@router.post("/terapias")
def topsis_terapias(payload: TopsisRequest):
    return TopsisService.evaluar(payload.matriz, payload.pesos, payload.tipos)
