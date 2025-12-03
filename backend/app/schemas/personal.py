from pydantic import BaseModel
from typing import Optional

class PersonalBase(BaseModel):
    usuario_id: int
    rol_id: int
    cedula_profesional: Optional[str] = None
    cedula_estatus: str = "NO_APLICA"
    especialidad: Optional[str] = None
    anio_experiencia: int = 0

class PersonalCreate(PersonalBase):
    pass

class PersonalUpdate(BaseModel):
    cedula_profesional: Optional[str] = None
    cedula_estatus: Optional[str] = None
    especialidad: Optional[str] = None
    anio_experiencia: Optional[int] = None

class PersonalRead(PersonalBase):
    id: int

    class Config:
        from_attributes = True
