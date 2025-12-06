# app/schemas/terapia.py

from typing import Optional, List
from pydantic import BaseModel
from enum import Enum


# =============================================================
# ENUM: Estado de la Terapia
# =============================================================
class EstadoTerapia(str, Enum):
    """
    Enum que representa el estado de una terapia.
    """
    ACTIVA = "ACTIVA"
    INACTIVA = "INACTIVA"


# =============================================================
# SCHEMAS: Terapia
# =============================================================
class TerapiaBase(BaseModel):
    """
    Datos base compartidos entre creación y lectura de terapias.
    """
    nombre: str
    descripcion: Optional[str] = None


class TerapiaCreate(TerapiaBase):
    """
    Schema para la creación de una nueva terapia.
    """
    pass


class TerapiaUpdate(BaseModel):
    """
    Schema para actualizar una terapia.
    Todos los campos son opcionales.
    """
    nombre: Optional[str] = None
    descripcion: Optional[str] = None
    estado: Optional[EstadoTerapia] = None


class TerapiaRead(TerapiaBase):
    """
    Schema para lectura de una terapia existente.
    """
    id_terapia: int
    estado: EstadoTerapia

    class Config:
        from_attributes = True  # Permite convertir automáticamente de ORM a Pydantic


# =============================================================
# SCHEMA: Personal con Terapia
# =============================================================
class PersonalConTerapia(BaseModel):
    """
    Representa a un miembro del personal con su terapia asignada (si la hay).
    """
    id_personal: int
    nombre_completo: str
    especialidad: str
    id_terapia: Optional[int] = None
    nombre_terapia: Optional[str] = None

    class Config:
        from_attributes = True


# =============================================================
# SCHEMAS: Asignaciones de Terapia
# =============================================================
class AsignacionTerapiaBase(BaseModel):
    """
    Datos base de la asignación de una terapia a un personal.
    """
    id_personal: int
    id_terapia: int


class AsignacionTerapiaCreate(AsignacionTerapiaBase):
    """
    Schema para crear una asignación de terapia a un personal.
    """
    pass


class AsignacionTerapiaRead(AsignacionTerapiaBase):
    """
    Schema para leer una asignación existente.
    """
    id_asignacion: int

    class Config:
        from_attributes = True
