from pydantic import BaseModel
from typing import List, Optional

class UserInToken(BaseModel):
    id: int
    nombres: str
    apellido_paterno: str
    apellido_materno: Optional[str]
    email: str
    rol_id: int
    rol_nombre: Optional[str]
    permisos: List[str]

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class LoginResponse(BaseModel):
    token: Token
    user: UserInToken
