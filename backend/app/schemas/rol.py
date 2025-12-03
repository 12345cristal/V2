# app/schemas/rol.py
from pydantic import BaseModel


class RolBase(BaseModel):
    nombre: str
    descripcion: str | None = None
    activo: bool = True


class RolRead(RolBase):
    id: int

    class Config:
        from_attributes = True
