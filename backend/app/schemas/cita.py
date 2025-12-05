# app/schemas/cita.py
from pydantic import BaseModel
from typing import Optional, List
from datetime import date, time


class CitaBase(BaseModel):
    fecha: date
    hora_inicio: time
    hora_fin: time
    estado_id: int
    es_reposicion: bool = False
    motivo: Optional[str]
    diagnostico_presuntivo: Optional[str]
    observaciones: Optional[str]


class CitaCreate(CitaBase):
    nombreNino: Optional[str]
    tutorNombre: Optional[str]
    telefonoTutor1: Optional[str]
    telefonoTutor2: Optional[str]


class CitaUpdate(CitaBase):
    id: int


class CitaList(BaseModel):
    id: int
    fecha: date
    hora_inicio: time
    hora_fin: time
    estado: str
    nombreNino: Optional[str]
    tutorNombre: Optional[str]

    class Config:
        orm_mode = True


class CatalogosCitaResponse(BaseModel):
    estadosCita: List[dict]
