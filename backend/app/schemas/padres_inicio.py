# schemas/padres_inicio.py
from pydantic import BaseModel
from datetime import date, datetime
from typing import Optional
from uuid import UUID

class ProximaSesionSchema(BaseModel):
    fecha: date
    hora: str
    terapeuta: str
    tipo: str

class UltimoAvanceSchema(BaseModel):
    fecha: date
    descripcion: str
    porcentaje: int

class ObservacionSchema(BaseModel):
    fecha: datetime
    terapeuta: str
    resumen: str

class InicioPadreResponse(BaseModel):
    hijo_id: UUID
    hijo_nombre: str

    proxima_sesion: Optional[ProximaSesionSchema]
    ultimo_avance: Optional[UltimoAvanceSchema]
    pagos_pendientes: float
    documento_nuevo: bool
    ultima_observacion: Optional[ObservacionSchema]
