# app/schemas/auth.py
from pydantic import BaseModel, EmailStr

class LoginRequest(BaseModel):
    correo: EmailStr
    contrasena: str

class UserResponse(BaseModel):
    id: int
    nombres: str
    email: EmailStr
    rol_id: int

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

class LoginResponse(BaseModel):
    token: TokenResponse
    user: UserResponse
