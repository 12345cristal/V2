# app/schemas/cita.py
from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from datetime import date, time, datetime


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
    """Schema para crear una nueva cita con Google Calendar"""
    sincronizar_google_calendar: bool = Field(default=True, description="Sincronizar con Google Calendar")


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
    sincronizar_google_calendar: bool = Field(default=True, description="Actualizar en Google Calendar")


class CitaCancelar(BaseModel):
    """Schema para cancelar una cita"""
    motivo_cancelacion: str = Field(..., min_length=10, max_length=500)
    eliminar_de_google_calendar: bool = Field(default=True)


class CitaReprogramar(BaseModel):
    """Schema para reprogramar una cita"""
    nueva_fecha: date = Field(...)
    nueva_hora_inicio: time = Field(...)
    nueva_hora_fin: time = Field(...)
    motivo: Optional[str] = Field(None, max_length=500)
    actualizar_google_calendar: bool = Field(default=True)


class CitaRead(CitaBase):
    model_config = ConfigDict(from_attributes=True)
    
    id_cita: int
    nino_nombre: Optional[str] = None
    terapeuta_nombre: Optional[str] = None
    terapia_nombre: Optional[str] = None
    estado_nombre: Optional[str] = None
    
    # Campos de Google Calendar
    google_event_id: Optional[str] = None
    google_calendar_link: Optional[str] = None
    sincronizado_calendar: bool = False
    fecha_sincronizacion: Optional[datetime] = None
    
    # Confirmación y cancelación
    confirmada: bool = False
    fecha_confirmacion: Optional[datetime] = None
    fecha_cancelacion: Optional[datetime] = None
    motivo_cancelacion: Optional[str] = None


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
