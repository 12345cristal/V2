from pydantic import BaseModel

class PermisoBase(BaseModel):
    id: int
    codigo: str
    descripcion: str | None = None

class RolBase(BaseModel):
    id: int
    nombre: str
    descripcion: str | None = None
    activo: bool

class RolWithPermisos(RolBase):
    permisos: list[PermisoBase]
