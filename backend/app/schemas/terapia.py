# app/schemas/terapia.py
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


# ============================================================
# TIPO TERAPIA (Catálogo)
# ============================================================

class TipoTerapiaBase(BaseModel):
    codigo: str
    nombre: str


class TipoTerapiaRead(TipoTerapiaBase):
    id: int

    class Config:
        from_attributes = True


# ============================================================
# PRIORIDAD (Catálogo)
# ============================================================

class PrioridadBase(BaseModel):
    codigo: str
    nombre: str


class PrioridadRead(PrioridadBase):
    id: int

    class Config:
        from_attributes = True


# ============================================================
# TERAPIA
# ============================================================

class TerapiaBase(BaseModel):
    nombre: str = Field(..., min_length=1, max_length=100)
    descripcion: Optional[str] = None


class TerapiaCreate(TerapiaBase):
    tipo_id: int = Field(default=1)  # Por defecto, puede ser ajustado según catálogo
    duracion_minutos: int = Field(default=60)
    objetivo_general: Optional[str] = None


class TerapiaUpdate(BaseModel):
    nombre: Optional[str] = Field(None, min_length=1, max_length=100)
    descripcion: Optional[str] = None
    tipo_id: Optional[int] = None
    duracion_minutos: Optional[int] = None
    objetivo_general: Optional[str] = None
    activo: Optional[int] = None


class TerapiaRead(TerapiaBase):
    id_terapia: int
    tipo_id: int
    duracion_minutos: int
    objetivo_general: Optional[str] = None
    estado: str  # ACTIVA o INACTIVA (calculado desde activo)

    class Config:
        from_attributes = True
        populate_by_name = True

    @classmethod
    def from_orm_with_estado(cls, obj):
        """Convierte activo (1/0) a estado (ACTIVA/INACTIVA)"""
        data = {
            "id_terapia": obj.id,
            "nombre": obj.nombre,
            "descripcion": obj.descripcion,
            "tipo_id": obj.tipo_id,
            "duracion_minutos": obj.duracion_minutos,
            "objetivo_general": obj.objetivo_general,
            "estado": "ACTIVA" if obj.activo == 1 else "INACTIVA"
        }
        return cls(**data)


# ============================================================
# ASIGNACIÓN DE PERSONAL A TERAPIAS
# ============================================================

class TerapiaPersonalBase(BaseModel):
    id_personal: int
    id_terapia: int


class TerapiaPersonalCreate(TerapiaPersonalBase):
    pass


class TerapiaPersonalRead(TerapiaPersonalBase):
    id_asignacion: int = Field(alias="id")
    activo: int

    class Config:
        from_attributes = True
        populate_by_name = True


# ============================================================
# PERSONAL DISPONIBLE / ASIGNADO (Para vista de asignación)
# ============================================================

class PersonalDisponible(BaseModel):
    id_personal: int
    nombre_completo: str
    especialidad: Optional[str] = None


class PersonalAsignado(BaseModel):
    id_personal: int
    nombre_completo: str
    terapia: str
    id_terapia: int


# ============================================================
# TERAPIA ASIGNADA A NIÑO
# ============================================================

class TerapiaNinoBase(BaseModel):
    nino_id: int
    terapia_id: int
    prioridad_id: int
    frecuencia_semana: int


class TerapiaNinoCreate(TerapiaNinoBase):
    terapeuta_id: Optional[int] = None
    fecha_asignacion: Optional[str] = None


class TerapiaNinoUpdate(BaseModel):
    terapeuta_id: Optional[int] = None
    prioridad_id: Optional[int] = None
    frecuencia_semana: Optional[int] = None
    activo: Optional[int] = None


class TerapiaNinoRead(TerapiaNinoBase):
    id: int
    terapeuta_id: Optional[int] = None
    fecha_asignacion: Optional[str] = None
    activo: int

    class Config:
        from_attributes = True


# Respuesta completa con información relacionada
class TerapiaNinoResponse(BaseModel):
    """Respuesta completa de terapia asignada a niño"""
    id: int
    ninoId: int
    terapiaId: int
    terapeutaId: Optional[int]
    prioridadId: int
    frecuenciaSemana: int
    fechaAsignacion: Optional[str]
    activo: int
    terapiaNombre: Optional[str] = None
    terapiaDescripcion: Optional[str] = None
    terapiaDuracion: Optional[int] = None
    ninoNombre: Optional[str] = None
    terapeutaNombre: Optional[str] = None
    prioridadNombre: Optional[str] = None


# ============================================================
# SESIONES
# ============================================================

class SesionBase(BaseModel):
    fecha: str
    asistio: int = 1
    progreso: Optional[int] = None
    colaboracion: Optional[int] = None
    observaciones: Optional[str] = None


class SesionCreate(SesionBase):
    terapia_nino_id: int
    creado_por: Optional[int] = None


class SesionRead(SesionBase):
    id: int
    terapia_nino_id: int
    creado_por: Optional[int] = None

    class Config:
        from_attributes = True


# ============================================================
# REPOSICIONES
# ============================================================

class ReposicionBase(BaseModel):
    nino_id: int
    terapia_id: int
    fecha_original: str
    fecha_nueva: str
    motivo: Optional[str] = None


class ReposicionCreate(ReposicionBase):
    pass


class ReposicionUpdate(BaseModel):
    estado: str  # PENDIENTE, APROBADA, RECHAZADA


class ReposicionRead(ReposicionBase):
    id: int
    estado: str

    class Config:
        from_attributes = True
