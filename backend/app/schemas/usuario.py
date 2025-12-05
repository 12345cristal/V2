# app/schemas/usuario.py

from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime
from app.models.usuario import EstadoUsuarioEnum


# ========================
# BASE DEL USUARIO
# ========================
class UsuarioBase(BaseModel):
  id_personal: int
  username: str
  email: EmailStr
  rol_sistema: str
  estado: EstadoUsuarioEnum = EstadoUsuarioEnum.ACTIVO
  debe_cambiar_password: bool = False


# ========================
# CREAR USUARIO
# ========================
class UsuarioCreate(UsuarioBase):
  password: str


# ========================
# ACTUALIZAR DATOS GENERALES
# ========================
class UsuarioUpdate(BaseModel):
  username: Optional[str] = None
  rol_sistema: Optional[str] = None
  estado: Optional[EstadoUsuarioEnum] = None


# ========================
# ACTUALIZAR SOLO ESTADO
# ========================
class UsuarioEstadoUpdate(BaseModel):
  estado: EstadoUsuarioEnum


# ========================
# ACTUALIZAR SOLO PASSWORD
# ========================
class UsuarioPasswordUpdate(BaseModel):
  password: str
  debe_cambiar_password: bool = False


# ========================
# LECTURA / RESPUESTA
# ========================
class UsuarioRead(UsuarioBase):
  id_usuario: int
  fecha_creacion: datetime
  ultima_sesion: Optional[datetime] = None

  # campos adicionales para listados
  nombre_completo: Optional[str] = None
  nombre_rol_personal: Optional[str] = None
  estado_laboral: Optional[str] = None

  class Config:
    from_attributes = True
