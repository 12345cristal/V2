# app/schemas/usuario.py
from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime


# =========================
# BASE
# =========================
class UsuarioBase(BaseModel):
    nombres: str
    apellido_paterno: str
    apellido_materno: Optional[str] = None
    email: EmailStr
    telefono: Optional[str] = None


# =========================
# CREATE
# =========================
class UsuarioCreate(UsuarioBase):
    password: str
    rol_id: int
    id_personal: Optional[int] = None


# =========================
# UPDATE
# =========================
class UsuarioUpdate(BaseModel):
    nombres: Optional[str] = None
    apellido_paterno: Optional[str] = None
    apellido_materno: Optional[str] = None
    email: Optional[EmailStr] = None
    telefono: Optional[str] = None
    activo: Optional[bool] = None
    rol_id: Optional[int] = None


# =========================
# LISTADO (TABLAS / GRIDS)
# =========================
class UsuarioListado(BaseModel):
    id_usuario: int
    id_personal: Optional[int]
    email: EmailStr
    nombre_completo: str
    rol_id: int
    nombre_rol: str
    estado: str
    estado_laboral: Optional[str] = None
    ultima_sesion: Optional[str] = None
    fecha_creacion: Optional[str] = None

    class Config:
        from_attributes = True


# =========================
# DETALLE
# =========================
class UsuarioDetalle(BaseModel):
    id_usuario: int
    email: EmailStr
    nombres: str
    apellido_paterno: str
    apellido_materno: Optional[str]
    rol_id: int
    nombre_rol: Optional[str]
    telefono: Optional[str]
    activo: bool
    fecha_creacion: Optional[str]

    class Config:
        from_attributes = True
