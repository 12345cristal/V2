# app/schemas/cita.py
from pydantic import BaseModel, Field
from typing import Optional
from datetime import date, time


# ============================================================
# ESTADO CITA (Catálogo)
# ============================================================

class EstadoCitaRead(BaseModel):
    id: int
    codigo: str
    nombre: str

    class Config:
        from_attributes = True


# ============================================================
# CITA
# ============================================================

class CitaBase(BaseModel):
    nino_id: int
    terapeuta_id: int
    terapia_id: int
    fecha: date
    hora_inicio: time
    hora_fin: time
    estado_id: int = Field(default=1)  # Por defecto PROGRAMADA
    motivo: Optional[str] = None
    observaciones: Optional[str] = None
    es_reposicion: int = Field(default=0)


class CitaCreate(CitaBase):
    pass


class CitaUpdate(BaseModel):
    nino_id: Optional[int] = None
    terapeuta_id: Optional[int] = None
    terapia_id: Optional[int] = None
    fecha: Optional[date] = None
    hora_inicio: Optional[time] = None
    hora_fin: Optional[time] = None
    estado_id: Optional[int] = None
    motivo: Optional[str] = None
    observaciones: Optional[str] = None
    es_reposicion: Optional[int] = None


class CitaRead(CitaBase):
    id_cita: int
    nino_nombre: Optional[str] = None
    terapeuta_nombre: Optional[str] = None
    terapia_nombre: Optional[str] = None
    estado_nombre: Optional[str] = None

    class Config:
        from_attributes = True


# ============================================================
# RESPUESTAS CON INFORMACIÓN COMPLETA
# ============================================================

class CitaDetalle(CitaRead):
    """Cita con información detallada del niño, terapeuta y terapia"""
    pass


class CitaListResponse(BaseModel):
    """Respuesta de lista de citas con paginación"""
    items: list[CitaRead]
    total: int
    page: int
    page_size: int
