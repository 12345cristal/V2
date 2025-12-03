# app/schemas/permiso.py
from pydantic import BaseModel


class PermisoBase(BaseModel):
    codigo: str
    descripcion: str | None = None


class PermisoRead(PermisoBase):
    id: int

    class Config:
        from_attributes = True
