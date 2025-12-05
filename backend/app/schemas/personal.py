from pydantic import BaseModel
from typing import Optional


class RolSchema(BaseModel):
    id_rol: int
    nombre_rol: str

    class Config:
        from_attributes = True


class PersonalBase(BaseModel):
    id_personal: int
    nombres: str
    apellido_paterno: str
    apellido_materno: Optional[str]
    especialidad_principal: str
    telefono_personal: str
    correo_personal: str
    estado_laboral: Optional[str]
    foto_url: Optional[str]
    experiencia: Optional[str]
    rating: Optional[float]

    class Config:
        from_attributes = True


class PersonalDetalle(BaseModel):
    id_personal: int
    nombres: str
    apellido_paterno: str
    apellido_materno: Optional[str]
    fecha_ingreso: str
    fecha_nacimiento: str

    especialidad_principal: str
    telefono_personal: str
    correo_personal: str

    rfc: str
    curp: str

    domicilio_calle: str
    domicilio_colonia: str
    domicilio_cp: str
    domicilio_municipio: str
    domicilio_estado: str

    experiencia: Optional[str]
    foto_url: Optional[str]

    class Config:
        from_attributes = True
