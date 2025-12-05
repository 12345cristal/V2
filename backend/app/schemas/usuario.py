# app/schemas/usuario.py
from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime
from app.models.usuario import EstadoUsuarioEnum


class UsuarioBase(BaseModel):
    id_personal: int
    username: str
    email: EmailStr
    rol_sistema: str
    estado: EstadoUsuarioEnum = EstadoUsuarioEnum.ACTIVO
    debe_cambiar_password: bool = False


class UsuarioCreate(UsuarioBase):
    password: str


class UsuarioUpdate(BaseModel):
    username: Optional[str] = None
    rol_sistema: Optional[str] = None
    estado: Optional[EstadoUsuarioEnum] = None


class UsuarioRead(UsuarioBase):
    id_usuario: int
    fecha_creacion: datetime
    ultima_sesion: Optional[datetime] = None

    class Config:
        from_attributes = True
