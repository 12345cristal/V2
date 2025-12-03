# app/schemas/usuario.py
from pydantic import BaseModel, EmailStr
from typing import List

from app.schemas.rol import RolRead


class UsuarioBase(BaseModel):
    nombres: str
    apellido_paterno: str
    apellido_materno: str | None = None
    email: EmailStr
    telefono: str | None = None
    activo: bool = True


class UsuarioCreate(UsuarioBase):
    password: str
    rol_id: int


class UsuarioUpdate(BaseModel):
    nombres: str | None = None
    apellido_paterno: str | None = None
    apellido_materno: str | None = None
    email: EmailStr | None = None
    telefono: str | None = None
    activo: bool | None = None
    rol_id: int | None = None
    password: str | None = None   # <- opcional si quieres cambiar pass desde UI


class UsuarioRead(UsuarioBase):
    id: int
    rol: RolRead | None = None
    permisos: List[str] = []

    class Config:
        from_attributes = True
