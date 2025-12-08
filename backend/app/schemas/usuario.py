# app/schemas/usuario.py
from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime


class UsuarioBase(BaseModel):
    """Schema base de Usuario"""
    nombres: str
    apellido_paterno: str
    apellido_materno: Optional[str] = None
    email: EmailStr
    telefono: Optional[str] = None


class UsuarioCreate(UsuarioBase):
    """Schema para crear un usuario"""
    password: str
    rol_id: int


class UsuarioUpdate(BaseModel):
    """Schema para actualizar un usuario"""
    nombres: Optional[str] = None
    apellido_paterno: Optional[str] = None
    apellido_materno: Optional[str] = None
    email: Optional[EmailStr] = None
    telefono: Optional[str] = None
    activo: Optional[bool] = None
    rol_id: Optional[int] = None


class Usuario(UsuarioBase):
    """Schema completo de Usuario"""
    id: int
    rol_id: int
    activo: bool
    fecha_creacion: datetime
    ultimo_login: Optional[datetime] = None
    
    class Config:
        from_attributes = True
