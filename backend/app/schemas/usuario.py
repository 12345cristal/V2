# app/schemas/usuario.py

from typing import Optional
from pydantic import BaseModel, EmailStr
from datetime import datetime
from enum import Enum


# =============================================================
# ENUM: Estado del Usuario
# =============================================================
class EstadoUsuario(str, Enum):
    ACTIVO = "ACTIVO"
    INACTIVO = "INACTIVO"
    BLOQUEADO = "BLOQUEADO"


# =============================================================
# BASE DEL USUARIO
# =============================================================
class UsuarioBase(BaseModel):
    """
    Datos base de un usuario compartidos entre creación y lectura.
    """
    id_personal: int
    username: str
    email: Optional[EmailStr] = None
    rol_sistema: str
    estado: EstadoUsuario = EstadoUsuario.ACTIVO
    debe_cambiar_password: bool = False


# =============================================================
# CREACIÓN DE USUARIO
# =============================================================
class UsuarioCreate(UsuarioBase):
    """
    Datos requeridos para crear un nuevo usuario.
    """
    password: str
    debe_cambiar_password: bool = True


# =============================================================
# ACTUALIZACIÓN DE DATOS GENERALES
# =============================================================
class UsuarioUpdate(BaseModel):
    """
    Campos opcionales para actualizar un usuario.
    """
    username: Optional[str] = None
    rol_sistema: Optional[str] = None
    estado: Optional[EstadoUsuario] = None


# =============================================================
# ACTUALIZAR SOLO ESTADO
# =============================================================
class UsuarioEstadoUpdate(BaseModel):
    """
    Permite actualizar únicamente el estado de un usuario.
    """
    estado: EstadoUsuario


# =============================================================
# ACTUALIZAR SOLO CONTRASEÑA
# =============================================================
class UsuarioPasswordUpdate(BaseModel):
    """
    Permite actualizar la contraseña y el flag de cambio obligatorio.
    """
    password: str
    debe_cambiar_password: bool = False


# =============================================================
# LECTURA / RESPUESTA DE USUARIO
# =============================================================
class UsuarioRead(UsuarioBase):
    """
    Representa los datos completos de un usuario para lectura.
    """
    id_usuario: int
    fecha_creacion: datetime
    ultima_sesion: Optional[datetime] = None

    # Campos adicionales opcionales para listados
    nombre_completo: Optional[str] = None
    nombre_rol_personal: Optional[str] = None
    estado_laboral: Optional[str] = None

    class Config:
        from_attributes = True


# =============================================================
# USUARIO PARA LISTADOS DETALLADOS
# =============================================================
class UsuarioListado(UsuarioRead):
    """
    Representa un usuario con información extendida para listados.
    """
    nombre_completo: str
    nombre_rol_personal: Optional[str] = None
    estado_laboral: Optional[str] = None
