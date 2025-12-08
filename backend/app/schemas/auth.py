# app/schemas/auth.py
from pydantic import BaseModel, EmailStr
from typing import List, Optional


class LoginRequest(BaseModel):
    """Schema para la petición de login"""
    email: EmailStr
    password: str


class Token(BaseModel):
    """Schema para el token JWT"""
    access_token: str
    token_type: str


class TokenData(BaseModel):
    """Schema para los datos decodificados del token"""
    user_id: Optional[int] = None
    email: Optional[str] = None
    rol_id: Optional[int] = None


class UserInToken(BaseModel):
    """Schema para los datos del usuario en el token"""
    id: int
    nombres: str
    apellido_paterno: str
    apellido_materno: Optional[str] = None
    email: str
    rol_id: int
    rol_nombre: Optional[str] = None
    permisos: List[str] = []
    
    class Config:
        from_attributes = True


class LoginResponse(BaseModel):
    """Schema para la respuesta del login"""
    token: Token
    user: UserInToken
