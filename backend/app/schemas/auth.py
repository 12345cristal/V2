# app/schemas/auth.py
from pydantic import BaseModel, EmailStr
from typing import List, Optional


# ---------- REQUEST ----------

class LoginRequest(BaseModel):
    email: EmailStr
    password: str


# ---------- USER RES ----------

class UserResponse(BaseModel):
    id: int
    nombres: str
    apellido_paterno: str
    apellido_materno: Optional[str] = None
    email: EmailStr
    rol_id: int
    rol_nombre: Optional[str] = None
    permisos: List[str] = []

    class Config:
        orm_mode = True


# ---------- TOKEN ----------

class TokenData(BaseModel):
    access_token: str
    token_type: str = "bearer"
    refresh_token: Optional[str] = None


class LoginResponse(BaseModel):
    token: TokenData
    user: UserResponse
