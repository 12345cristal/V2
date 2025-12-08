"""
Schemas de Pydantic para Cita
"""

from datetime import date, time, datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict


# ============= CITA SCHEMAS =============

class CitaBase(BaseModel):
    nino_id: int
    terapia_id: int
    personal_id: int
    fecha: date
    hora_inicio: time
    hora_fin: Optional[time] = None
    estado_cita_id: int
    motivo: Optional[str] = None
    observaciones: Optional[str] = None


class CitaCreate(CitaBase):
    pass


class CitaUpdate(BaseModel):
    nino_id: Optional[int] = None
    terapia_id: Optional[int] = None
    personal_id: Optional[int] = None
    fecha: Optional[date] = None
    hora_inicio: Optional[time] = None
    hora_fin: Optional[time] = None
    estado_cita_id: Optional[int] = None
    motivo: Optional[str] = None
    observaciones: Optional[str] = None


class CitaInDB(CitaBase):
    id: int
    fecha_creacion: datetime
    
    model_config = ConfigDict(from_attributes=True)


class CitaWithDetails(CitaInDB):
    """Cita con información relacionada"""
    nino_nombre: Optional[str] = None
    terapeuta_nombre: Optional[str] = None
    terapia_nombre: Optional[str] = None
    estado_nombre: Optional[str] = None


class CitaList(BaseModel):
    """Schema mínimo para listados"""
    id: int
    nino_id: int
    nino_nombre: Optional[str] = None
    fecha: date
    hora_inicio: time
    hora_fin: Optional[time] = None
    estado_nombre: Optional[str] = None
    terapeuta_nombre: Optional[str] = None
    
    model_config = ConfigDict(from_attributes=True)


class CitaCancelar(BaseModel):
    """Schema para cancelar cita"""
    motivo_cancelacion: str
