# app/schemas/auth.py
from pydantic import BaseModel, EmailStr
from typing import List


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UserInToken(BaseModel):
    id: int
    nombres: str
    apellido_paterno: str
    apellido_materno: str | None
    email: EmailStr
    rol_id: int | None
    rol_nombre: str | None
    permisos: List[str]


class LoginResponse(BaseModel):
    token: Token
    user: UserInToken
