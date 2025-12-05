from pydantic import BaseModel
from typing import Optional


class TerapiaSchema(BaseModel):
    id_terapia: int
    nombre: str
    descripcion: Optional[str]
    activo: bool

    class Config:
        from_attributes = True


class TerapiaCreateRequest(BaseModel):
    nombre: str
    descripcion: Optional[str] = None


class TerapiaUpdateRequest(TerapiaCreateRequest):
    pass


class PersonalAsignadoSchema(BaseModel):
    id_personal: int
    nombres: str
    apellido_paterno: str
    apellido_materno: Optional[str]
    especialidad_principal: str
    id_terapia: int

    class Config:
        from_attributes = True


class AsignarPersonalRequest(BaseModel):
    id_personal: int
    id_terapia: int
