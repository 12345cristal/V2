# app/schemas/auth.py
from pydantic import BaseModel
from typing import List, Optional


class UserInToken(BaseModel):
    id: int
    nombres: str
    apellido_paterno: str
    apellido_materno: Optional[str] = None
    email: str
    rol_id: int
    rol_nombre: Optional[str] = None
    permisos: List[str]


class LoginResponse(BaseModel):
    token: dict
    user: UserInToken
