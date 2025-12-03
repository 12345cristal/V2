from pydantic import BaseModel
from typing import Optional, List

class TerapiaBase(BaseModel):
    nombre: str
    descripcion: Optional[str] = None
    tipo_terapia_id: int
    duracion_minutos: int
    objetivo_general: str
    activo: bool = True


class TerapiaCreate(TerapiaBase):
    pass


class TerapiaUpdate(BaseModel):
    nombre: Optional[str] = None
    descripcion: Optional[str] = None
    tipo_terapia_id: Optional[int] = None
    duracion_minutos: Optional[int] = None
    objetivo_general: Optional[str] = None
    activo: Optional[bool] = None


class TerapiaRead(TerapiaBase):
    id: int

    class Config:
        from_attributes = True


class PersonalAsignado(BaseModel):
    id: int
    personal_id: int
    nombre_completo: str

    class Config:
        from_attributes = True
