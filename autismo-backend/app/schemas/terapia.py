"""
Schemas de Pydantic para Terapia, Sesión y Reposición
"""

from datetime import date, datetime, time
from typing import Optional, List
from decimal import Decimal
from pydantic import BaseModel, ConfigDict


# ============= TERAPIA SCHEMAS =============

class TerapiaBase(BaseModel):
    tipo_terapia_id: int
    nombre: str
    descripcion: Optional[str] = None
    duracion_minutos: Optional[int] = None
    costo: Optional[Decimal] = None


class TerapiaCreate(TerapiaBase):
    pass


class TerapiaUpdate(BaseModel):
    tipo_terapia_id: Optional[int] = None
    nombre: Optional[str] = None
    descripcion: Optional[str] = None
    duracion_minutos: Optional[int] = None
    costo: Optional[Decimal] = None


class TerapiaInDB(TerapiaBase):
    id: int
    
    model_config = ConfigDict(from_attributes=True)


# ============= TERAPIA_PERSONAL SCHEMAS =============

class TerapiaPersonalBase(BaseModel):
    terapia_id: int
    personal_id: int


class TerapiaPersonalCreate(TerapiaPersonalBase):
    pass


class TerapiaPersonalInDB(TerapiaPersonalBase):
    id: int
    
    model_config = ConfigDict(from_attributes=True)


# ============= TERAPIA_NINO SCHEMAS =============

class TerapiaNinoBase(BaseModel):
    nino_id: int
    terapia_id: int
    fecha_inicio: date
    fecha_fin: Optional[date] = None
    sesiones_semanales: Optional[int] = None
    estatus: Optional[str] = "ACTIVA"
    objetivo_general: Optional[str] = None


class TerapiaNinoCreate(TerapiaNinoBase):
    pass


class TerapiaNinoUpdate(BaseModel):
    fecha_inicio: Optional[date] = None
    fecha_fin: Optional[date] = None
    sesiones_semanales: Optional[int] = None
    estatus: Optional[str] = None
    objetivo_general: Optional[str] = None


class TerapiaNinoInDB(TerapiaNinoBase):
    id: int
    
    model_config = ConfigDict(from_attributes=True)


# ============= SESION SCHEMAS =============

class SesionBase(BaseModel):
    terapia_nino_id: int
    personal_id: int
    fecha: date
    hora_inicio: time
    hora_fin: Optional[time] = None
    estatus: Optional[str] = "PENDIENTE"
    objetivo_sesion: Optional[str] = None
    actividades_realizadas: Optional[str] = None
    observaciones: Optional[str] = None
    progreso: Optional[str] = None


class SesionCreate(SesionBase):
    pass


class SesionUpdate(BaseModel):
    fecha: Optional[date] = None
    hora_inicio: Optional[time] = None
    hora_fin: Optional[time] = None
    estatus: Optional[str] = None
    objetivo_sesion: Optional[str] = None
    actividades_realizadas: Optional[str] = None
    observaciones: Optional[str] = None
    progreso: Optional[str] = None


class SesionInDB(SesionBase):
    id: int
    
    model_config = ConfigDict(from_attributes=True)


class SesionWithDetails(SesionInDB):
    """Sesión con información adicional"""
    nino_nombre: Optional[str] = None
    terapeuta_nombre: Optional[str] = None
    terapia_nombre: Optional[str] = None


# ============= REPOSICION SCHEMAS =============

class ReposicionBase(BaseModel):
    sesion_id: int
    fecha_original: date
    fecha_reposicion: Optional[date] = None
    motivo: str
    aprobado: Optional[int] = 0
    observaciones: Optional[str] = None


class ReposicionCreate(ReposicionBase):
    pass


class ReposicionUpdate(BaseModel):
    fecha_reposicion: Optional[date] = None
    motivo: Optional[str] = None
    aprobado: Optional[int] = None
    observaciones: Optional[str] = None


class ReposicionInDB(ReposicionBase):
    id: int
    
    model_config = ConfigDict(from_attributes=True)


# ============= SCHEMAS COMPUESTOS =============

class TerapiaCompleta(TerapiaInDB):
    """Terapia con información de tipo"""
    tipo_terapia_nombre: Optional[str] = None
    terapeutas: List[int] = []  # IDs de personal asignado


class TerapiaNinoCompleta(TerapiaNinoInDB):
    """Terapia de niño con detalles"""
    nino_nombre: Optional[str] = None
    terapia_nombre: Optional[str] = None
    tipo_terapia_nombre: Optional[str] = None
    total_sesiones: Optional[int] = 0


class SesionList(BaseModel):
    """Schema mínimo para listados de sesiones"""
    id: int
    fecha: date
    hora_inicio: time
    hora_fin: Optional[time] = None
    estatus: Optional[str] = None
    nino_nombre: Optional[str] = None
    terapeuta_nombre: Optional[str] = None
    
    model_config = ConfigDict(from_attributes=True)
