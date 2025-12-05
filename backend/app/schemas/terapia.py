# app/schemas/terapia.py

from pydantic import BaseModel
from typing import Optional


class TerapiaBase(BaseModel):
    nombre: str
    descripcion: str
    estado: str = "ACTIVA"


class TerapiaCreate(TerapiaBase):
    pass


class TerapiaUpdate(BaseModel):
    nombre: Optional[str] = None
    descripcion: Optional[str] = None
    estado: Optional[str] = None


class TerapiaRead(TerapiaBase):
    id_terapia: int

    class Config:
        from_attributes = True


class PersonalConTerapia(BaseModel):
    id_personal: int
    nombre_completo: str
    especialidad: str
    id_terapia: Optional[int] = None

    class Config:
        from_attributes = True
