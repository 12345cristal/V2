# app/schemas/usuario.py
from datetime import datetime
from pydantic import BaseModel, EmailStr, ConfigDict


class UsuarioBase(BaseModel):
    nombres: str
    apellido_paterno: str
    apellido_materno: str | None = None
    email: EmailStr
    telefono: str | None = None
    rol_id: int


class UsuarioCreate(UsuarioBase):
    password: str


class UsuarioUpdate(BaseModel):
    nombres: str | None = None
    apellido_paterno: str | None = None
    apellido_materno: str | None = None
    telefono: str | None = None
    rol_id: int | None = None
    activo: bool | None = None


class UsuarioRead(UsuarioBase):
    id: int
    activo: bool
    fecha_creacion: datetime
    ultimo_login: datetime | None

    model_config = ConfigDict(from_attributes=True)
