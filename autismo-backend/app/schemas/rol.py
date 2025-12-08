"""
Schemas de Pydantic para Rol y Permiso
"""

from typing import Optional, List
from pydantic import BaseModel, ConfigDict


# ============= PERMISO SCHEMAS =============

class PermisoBase(BaseModel):
    codigo: str
    descripcion: Optional[str] = None


class PermisoCreate(PermisoBase):
    pass


class PermisoUpdate(BaseModel):
    codigo: Optional[str] = None
    descripcion: Optional[str] = None


class PermisoInDB(PermisoBase):
    id: int
    
    model_config = ConfigDict(from_attributes=True)


# ============= ROL SCHEMAS =============

class RolBase(BaseModel):
    nombre: str
    descripcion: Optional[str] = None


class RolCreate(RolBase):
    pass


class RolUpdate(BaseModel):
    nombre: Optional[str] = None
    descripcion: Optional[str] = None


class RolInDB(RolBase):
    id: int
    
    model_config = ConfigDict(from_attributes=True)


# Schema con permisos incluidos
class RolWithPermisos(RolInDB):
    permisos: List[PermisoInDB] = []


# ============= ROLE_PERMISO SCHEMAS =============

class RolePermisoAssign(BaseModel):
    """Schema para asignar/desasignar permisos a un rol"""
    permiso_ids: List[int]
