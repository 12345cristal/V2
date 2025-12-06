from pydantic import BaseModel
from typing import Dict, List


class PrioridadRequest(BaseModel):
    max_resultados: int = 10

    peso_prioridad: float = 0.4          # beneficio
    peso_tiempo_espera: float = 0.3      # beneficio
    peso_asistencias: float = 0.15       # beneficio
    peso_inasistencias: float = 0.15     # costo


class NinoPrioritario(BaseModel):
    id_nino: int
    nombre_completo: str
    score: float
    rank: int
    criterios: Dict[str, float]
