# app/schemas/coordinador.py
from pydantic import BaseModel
from typing import List, Optional, Literal

class TarjetaIndicador(BaseModel):
    titulo: str
    valor: int
    unidad: Optional[str] = None
    tendencia: Optional[Literal['up', 'down', 'flat']] = 'flat'

class TerapeutaResumenMini(BaseModel):
    id_personal: int
    nombre_completo: str
    especialidad: str
    pacientes: int
    sesiones_semana: int
    rating: Optional[float] = None

class NinoRiesgo(BaseModel):
    id_nino: int
    nombre_completo: str
    motivo: str
    prioridad: Literal['ALTA', 'MEDIA', 'BAJA']

class DashboardCoordinador(BaseModel):
    fecha: str
    indicadores: List[TarjetaIndicador]
    topTerapeutas: List[TerapeutaResumenMini]
    ninosEnRiesgo: List[NinoRiesgo]
    resumenIA: Optional[str] = None
