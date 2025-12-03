# app/schemas/cita.py
from datetime import date, time
from typing import Optional, List

from pydantic import BaseModel, ConfigDict, field_validator


class CitaBase(BaseModel):
    fecha: date
    hora_inicio: time
    hora_fin: time
    terapeuta_id: Optional[int] = None
    terapia_id: Optional[int] = None
    estado_id: Optional[int] = None  # si viene null, se pone AGENDADA
    es_reposicion: bool = False
    motivo: Optional[str] = None
    diagnostico_presuntivo: Optional[str] = None
    observaciones: Optional[str] = None

    # Niño existente
    nino_id: Optional[int] = None

    # Bandera nuevo niño
    es_nuevo_nino: bool = False

    # Datos temporales
    temp_nino_nombre: Optional[str] = None
    temp_nino_apellido_paterno: Optional[str] = None
    temp_nino_apellido_materno: Optional[str] = None
    temp_tutor_nombre: Optional[str] = None
    temp_tutor_apellido_paterno: Optional[str] = None
    temp_tutor_apellido_materno: Optional[str] = None
    telefono_temporal: Optional[str] = None

    @field_validator("hora_fin")
    @classmethod
    def validar_horas(cls, v, info):
        hora_inicio = info.data.get("hora_inicio")
        if hora_inicio and v <= hora_inicio:
            raise ValueError("La hora de fin debe ser mayor a la de inicio")
        return v

    @field_validator("es_nuevo_nino")
    @classmethod
    def validar_nino(cls, es_nuevo, info):
        nino_id = info.data.get("nino_id")

        if es_nuevo and nino_id:
            raise ValueError("No puede tener nino_id y es_nuevo_nino=True al mismo tiempo")

        # Si es nuevo niño, validar que venga al menos nombre y tutor
        if es_nuevo:
            if not info.data.get("temp_nino_nombre") or not info.data.get("temp_tutor_nombre"):
                raise ValueError("Debe proporcionar nombre del niño y del tutor para nuevo niño")

        return es_nuevo


class CitaCreate(CitaBase):
    pass


class CitaUpdate(BaseModel):
    fecha: Optional[date] = None
    hora_inicio: Optional[time] = None
    hora_fin: Optional[time] = None
    terapeuta_id: Optional[int] = None
    terapia_id: Optional[int] = None
    estado_id: Optional[int] = None
    es_reposicion: Optional[bool] = None
    motivo: Optional[str] = None
    diagnostico_presuntivo: Optional[str] = None
    observaciones: Optional[str] = None
    nino_id: Optional[int] = None


class CitaRead(BaseModel):
    id: int

    fecha: date
    hora_inicio: time
    hora_fin: time

    nino_id: Optional[int]
    es_nuevo_nino: bool
    nombre_mostrado: str

    terapeuta_id: Optional[int]
    terapeuta_nombre: Optional[str]

    terapia_id: Optional[int]
    terapia_nombre: Optional[str]

    estado_id: int
    estado_codigo: str
    estado_nombre: str

    es_reposicion: bool
    motivo: Optional[str]
    diagnostico_presuntivo: Optional[str]
    observaciones: Optional[str]

    model_config = ConfigDict(from_attributes=True)


class CitaObservadorRead(BaseModel):
    id: int
    terapeuta_id: int
    terapeuta_nombre: str

    model_config = ConfigDict(from_attributes=True)
