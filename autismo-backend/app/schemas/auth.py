from pydantic import BaseModel, EmailStr, ConfigDict
from typing import List, Optional
from datetime import datetime


class LoginRequest(BaseModel):
    """Request de login"""
    email: EmailStr
    password: str


class Token(BaseModel):
    """Token JWT"""
    access_token: str
    token_type: str = "bearer"


class UserInToken(BaseModel):
    """Usuario en el token/respuesta de login"""
    id: int
    nombres: str
    apellido_paterno: str
    apellido_materno: Optional[str] = None
    email: str
    rol_id: int
    rol_nombre: Optional[str] = None
    permisos: List[str] = []
    
    model_config = ConfigDict(from_attributes=True)


class LoginResponse(BaseModel):
    """Respuesta completa del login"""
    token: Token
    user: UserInToken


class ChangePasswordRequest(BaseModel):
    """Request para cambiar contraseña"""
    current_password: str
    new_password: str
