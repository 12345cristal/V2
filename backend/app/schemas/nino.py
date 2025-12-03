# app/schemas/nino.py
from datetime import date, datetime
from pydantic import BaseModel, ConfigDict


class NinoBase(BaseModel):
    nombre: str
    apellido_paterno: str
    apellido_materno: str | None = None
    fecha_nacimiento: date
    sexo: str  # "M" | "F" | "O"
    curp: str | None = None
    tutor_principal_id: int | None = None


class NinoCreate(NinoBase):
    pass


class NinoUpdate(BaseModel):
    nombre: str | None = None
    apellido_paterno: str | None = None
    apellido_materno: str | None = None
    estado: str | None = None
    tutor_principal_id: int | None = None


class NinoRead(NinoBase):
    id: int
    estado: str
    fecha_registro: datetime

    model_config = ConfigDict(from_attributes=True)
