from pydantic import BaseModel
from typing import Optional


class RolSchema(BaseModel):
    id_rol: int
    nombre_rol: str

    class Config:
        from_attributes = True


class PersonalSimple(BaseModel):
    id_personal: int
    nombres: str
    apellido_paterno: str
    apellido_materno: Optional[str]
    especialidad_principal: Optional[str]

    class Config:
        from_attributes = True


class UsuarioListado(BaseModel):
    id_usuario: int
    username: str
    estado: str
    rol_sistema: str
    id_personal: Optional[int]
    nombres: Optional[str]
    apellido_paterno: Optional[str]
    apellido_materno: Optional[str]

    class Config:
        from_attributes = True


class UsuarioDetalle(BaseModel):
    id_usuario: int
    username: str
    estado: str
    rol_sistema: str
    id_personal: int

    debe_cambiar_password: bool

    class Config:
        from_attributes = True


class UsuarioCreateRequest(BaseModel):
    id_personal: int
    username: str
    rol_sistema: str
    estado: str

    password: str
    confirmarPassword: str


class UsuarioUpdateRequest(BaseModel):
    id_personal: int
    username: str
    rol_sistema: str
    estado: str

    cambiarPassword: bool = False
    password: Optional[str] = None
    confirmarPassword: Optional[str] = None
