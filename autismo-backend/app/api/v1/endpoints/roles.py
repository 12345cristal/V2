"""
Endpoints para gestión de roles y permisos
"""

from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.core.security import require_permissions
from app.services import rol_service
from app.schemas.rol import (
    RolCreate,
    RolUpdate,
    RolInDB,
    RolWithPermisos,
    PermisoInDB,
    RolePermisoAssign,
)


router = APIRouter()


@router.get("/roles", response_model=List[RolInDB])
async def listar_roles(
    db: Session = Depends(get_db),
    _: None = Depends(require_permissions("roles:ver")),
):
    """
    Listar todos los roles del sistema.
    
    **Permisos requeridos:** `roles:ver`
    """
    return rol_service.get_roles(db=db)


@router.post("/roles", response_model=RolInDB, status_code=status.HTTP_201_CREATED)
async def crear_rol(
    rol_data: RolCreate,
    db: Session = Depends(get_db),
    _: None = Depends(require_permissions("roles:editar")),
):
    """
    Crear nuevo rol.
    
    **Permisos requeridos:** `roles:editar`
    
    **Nota:** El rol se crea sin permisos. Use el endpoint de asignación de permisos.
    """
    return rol_service.create_rol(db=db, rol_data=rol_data)


@router.get("/roles/{rol_id}", response_model=RolWithPermisos)
async def obtener_rol(
    rol_id: int,
    db: Session = Depends(get_db),
    _: None = Depends(require_permissions("roles:ver")),
):
    """
    Obtener rol por ID con sus permisos.
    
    **Permisos requeridos:** `roles:ver`
    """
    return rol_service.get_rol_with_permisos(db=db, rol_id=rol_id)


@router.put("/roles/{rol_id}", response_model=RolInDB)
async def actualizar_rol(
    rol_id: int,
    rol_data: RolUpdate,
    db: Session = Depends(get_db),
    _: None = Depends(require_permissions("roles:editar")),
):
    """
    Actualizar nombre o descripción de un rol.
    
    **Permisos requeridos:** `roles:editar`
    """
    return rol_service.update_rol(db=db, rol_id=rol_id, rol_data=rol_data)


@router.post("/roles/{rol_id}/permisos", response_model=RolWithPermisos)
async def asignar_permisos_a_rol(
    rol_id: int,
    permisos_data: RolePermisoAssign,
    db: Session = Depends(get_db),
    _: None = Depends(require_permissions("roles:editar")),
):
    """
    Asignar permisos a un rol (reemplaza los permisos existentes).
    
    **Permisos requeridos:** `roles:editar`
    
    **Cuerpo de la petición:**
    ```json
    {
      "permiso_ids": [1, 2, 3, 5, 8]
    }
    ```
    
    **Nota:** Esta operación elimina los permisos anteriores y asigna los nuevos.
    """
    return rol_service.assign_permisos_to_rol(
        db=db,
        rol_id=rol_id,
        permiso_ids=permisos_data.permiso_ids,
    )


@router.get("/permisos", response_model=List[PermisoInDB])
async def listar_permisos(
    db: Session = Depends(get_db),
    _: None = Depends(require_permissions("roles:ver")),
):
    """
    Listar todos los permisos disponibles en el sistema.
    
    **Permisos requeridos:** `roles:ver`
    
    Use este endpoint para obtener los IDs de permisos al asignar a roles.
    """
    return rol_service.get_all_permisos(db=db)
