# app/schemas/auth.py
from pydantic import BaseModel, EmailStr, ConfigDict


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
    rol: str
    permisos: list[str]


class LoginResponse(BaseModel):
    token: Token
    user: UserInToken
