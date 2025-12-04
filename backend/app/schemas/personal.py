# app/schemas/personal.py
from pydantic import BaseModel
from datetime import date
from typing import Optional


class PersonalBase(BaseModel):
    nombres: str
    apellido_paterno: str
    apellido_materno: Optional[str] = None
    email: str
    telefono_personal: Optional[str]
    id_rol: int
    especialidad_principal: str
    fecha_ingreso: date
    fecha_nacimiento: date
    rfc: str
    curp: str
    experiencia: str
    domicilio_calle: str
    domicilio_colonia: str
    domicilio_cp: str
    domicilio_municipio: str
    domicilio_estado: str


class PersonalCreate(PersonalBase):
    pass


class PersonalUpdate(BaseModel):
    nombres: Optional[str] = None
    apellido_paterno: Optional[str] = None
    apellido_materno: Optional[str] = None
    email: Optional[str] = None
    telefono_personal: Optional[str] = None
    id_rol: Optional[int] = None
    especialidad_principal: Optional[str] = None
    fecha_ingreso: Optional[date] = None
    fecha_nacimiento: Optional[date] = None
    rfc: Optional[str] = None
    curp: Optional[str] = None
    experiencia: Optional[str] = None
    domicilio_calle: Optional[str] = None
    domicilio_colonia: Optional[str] = None
    domicilio_cp: Optional[str] = None
    domicilio_municipio: Optional[str] = None
    domicilio_estado: Optional[str] = None


class PersonalRead(BaseModel):
    id_personal: int
    nombres: str
    apellido_paterno: str
    apellido_materno: Optional[str]
    id_rol: int
    nombre_rol: str
    correo_personal: Optional[str]
    telefono_personal: Optional[str]
    especialidad_principal: Optional[str]
    estado_laboral: Optional[str]
    rating: Optional[float]
    foto_url: Optional[str] = None

    class Config:
        from_attributes = True
