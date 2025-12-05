from pydantic import BaseModel

class UsuarioBase(BaseModel):
    id: int
    nombres: str
    apellido_paterno: str
    apellido_materno: str | None
    email: str
    telefono: str | None
    activo: bool


class UsuarioCreate(BaseModel):
    nombres: str
    apellido_paterno: str
    apellido_materno: str | None
    email: str
    password: str
    rol_id: int


class UsuarioRead(UsuarioBase):
    rol_id: int
