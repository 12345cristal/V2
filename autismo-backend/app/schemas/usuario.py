"""
Schemas de Pydantic para Usuario
"""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, ConfigDict


# Schema base con campos comunes
class UsuarioBase(BaseModel):
    nombres: str
    apellido_paterno: str
    apellido_materno: Optional[str] = None
    email: EmailStr
    telefono: Optional[str] = None
    rol_id: int


# Schema para crear usuario (requiere contraseña)
class UsuarioCreate(UsuarioBase):
    password: str


# Schema para actualizar usuario (todos los campos opcionales)
class UsuarioUpdate(BaseModel):
    nombres: Optional[str] = None
    apellido_paterno: Optional[str] = None
    apellido_materno: Optional[str] = None
    email: Optional[EmailStr] = None
    telefono: Optional[str] = None
    rol_id: Optional[int] = None
    activo: Optional[int] = None


# Schema para cambiar contraseña
class UsuarioChangePassword(BaseModel):
    old_password: str
    new_password: str


# Schema para respuesta (incluye ID y campos de BD)
class UsuarioInDB(UsuarioBase):
    id: int
    activo: int
    fecha_registro: datetime
    ultimo_login: Optional[datetime] = None
    
    model_config = ConfigDict(from_attributes=True)


# Schema con datos de rol para respuesta completa
class UsuarioWithRol(UsuarioInDB):
    rol_nombre: Optional[str] = None


# Schema mínimo para listados
class UsuarioList(BaseModel):
    id: int
    nombres: str
    apellido_paterno: str
    apellido_materno: Optional[str] = None
    email: EmailStr
    telefono: Optional[str] = None
    activo: int
    rol_nombre: Optional[str] = None
    
    model_config = ConfigDict(from_attributes=True)
