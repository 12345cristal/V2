from typing import Dict, List
from pydantic import BaseModel, Field


class RecomendacionTerapeutaRequest(BaseModel):
    id_terapia: int = Field(..., description="Terapia para la que se quiere recomendar personal")
    max_resultados: int = Field(5, ge=1, le=50)

    # Pesos (se normalizan internamente)
    peso_carga: float = 0.3   # total_pacientes (costo)
    peso_sesiones: float = 0.2  # sesiones_semana (costo)
    peso_rating: float = 0.3    # rating (beneficio)
    peso_afinidad: float = 0.2  # afinidad terapia (beneficio)


class TerapeutaRecomendado(BaseModel):
    id_personal: int
    nombre_completo: str
    id_terapia: int
    terapia_nombre: str
    score: float
    rank: int
    criterios: Dict[str, float]
