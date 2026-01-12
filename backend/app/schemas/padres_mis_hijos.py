# app/schemas/padres_mis_hijos.py
from pydantic import BaseModel
from datetime import date, datetime
from typing import List, Optional


class AlergiaResponse(BaseModel):
    """Esquema de respuesta para alergia"""
    id: int
    nombre: str
    severidad: str  # leve, moderada, severa
    reaccion: str

    class Config:
        from_attributes = True


class MedicamentoResponse(BaseModel):
    """Esquema de respuesta para medicamento"""
    id: int
    nombre: str
    dosis: str
    frecuencia: str
    razon: str
    fechaInicio: date
    fechaFin: Optional[date] = None
    activo: bool
    novedadReciente: bool = False
    fechaActualizacion: Optional[datetime] = None

    class Config:
        from_attributes = True
        populate_by_name = True
        fields = {
            "fecha_inicio": {"alias": "fechaInicio"},
            "fecha_fin": {"alias": "fechaFin"},
            "fecha_actualizacion": {"alias": "fechaActualizacion"},
            "novedadReciente": {"alias": "novedadReciente"}
        }


class HijoResponse(BaseModel):
    """Esquema de respuesta para un hijo"""
    id: int
    nombre: str
    apellidoPaterno: str
    apellidoMaterno: Optional[str] = None
    foto: Optional[str] = None
    fechaNacimiento: date
    edad: Optional[int] = None
    diagnostico: Optional[str] = None
    cuatrimestre: Optional[int] = None
    fechaIngreso: Optional[date] = None
    alergias: List[AlergiaResponse] = []
    medicamentos: List[MedicamentoResponse] = []
    visto: bool = False
    novedades: int = 0

    class Config:
        from_attributes = True
        populate_by_name = True


class MisHijosPageResponse(BaseModel):
    """Esquema de respuesta para la página Mis Hijos"""
    hijos: List[HijoResponse] = []

    class Config:
        from_attributes = True


class MisHijosApiResponse(BaseModel):
    """Esquema de respuesta API para Mis Hijos"""
    exito: bool
    datos: Optional[MisHijosPageResponse] = None
    error: Optional[str] = None
    mensaje: Optional[str] = None

    class Config:
        from_attributes = True
