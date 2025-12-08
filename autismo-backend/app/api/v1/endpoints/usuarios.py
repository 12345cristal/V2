"""
Endpoints para gestión de usuarios
"""

from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.core.security import get_current_active_user, require_permissions
from app.models.usuario import Usuario
from app.services import usuario_service
from app.schemas.usuario import (
    UsuarioCreate,
    UsuarioUpdate,
    UsuarioInDB,
    UsuarioList,
    UsuarioWithRol,
)


router = APIRouter()


@router.get("/usuarios", response_model=dict)
async def listar_usuarios(
    skip: int = Query(0, ge=0, description="Número de registros a saltar"),
    limit: int = Query(100, ge=1, le=500, description="Número máximo de registros"),
    search: Optional[str] = Query(None, description="Buscar por nombre o email"),
    rol_id: Optional[int] = Query(None, description="Filtrar por rol"),
    activo: Optional[int] = Query(None, ge=0, le=1, description="Filtrar por estado activo (0 o 1)"),
    db: Session = Depends(get_db),
    _: None = Depends(require_permissions("usuarios:ver")),
):
    """
    Listar usuarios con filtros opcionales y paginación.
    
    **Permisos requeridos:** `usuarios:ver`
    
    **Filtros disponibles:**
    - search: Búsqueda por nombres, apellidos o email
    - rol_id: Filtrar por rol específico
    - activo: 0 para inactivos, 1 para activos
    
    **Retorna:**
    - items: Lista de usuarios
    - total: Total de usuarios que cumplen los filtros
    - skip: Offset usado
    - limit: Límite usado
    """
    usuarios = usuario_service.get_usuarios(
        db=db,
        skip=skip,
        limit=limit,
        search=search,
        rol_id=rol_id,
        activo=activo,
    )
    
    total = usuario_service.count_usuarios(
        db=db,
        search=search,
        rol_id=rol_id,
        activo=activo,
    )
    
    # Construir respuesta con información del rol
    usuarios_response = []
    for usuario in usuarios:
        usuario_dict = {
            "id": usuario.id,
            "nombres": usuario.nombres,
            "apellido_paterno": usuario.apellido_paterno,
            "apellido_materno": usuario.apellido_materno,
            "email": usuario.email,
            "telefono": usuario.telefono,
            "activo": usuario.activo,
            "rol_id": usuario.rol_id,
            "rol_nombre": usuario.rol.nombre if usuario.rol else None,
            "fecha_registro": usuario.fecha_registro,
            "ultimo_login": usuario.ultimo_login,
        }
        usuarios_response.append(usuario_dict)
    
    return {
        "items": usuarios_response,
        "total": total,
        "skip": skip,
        "limit": limit,
    }


@router.post("/usuarios", response_model=UsuarioWithRol, status_code=status.HTTP_201_CREATED)
async def crear_usuario(
    usuario_data: UsuarioCreate,
    db: Session = Depends(get_db),
    _: None = Depends(require_permissions("usuarios:crear")),
):
    """
    Crear nuevo usuario.
    
    **Permisos requeridos:** `usuarios:crear`
    
    **Validaciones:**
    - Email único
    - Rol válido
    - Contraseña mínimo 8 caracteres
    """
    usuario = usuario_service.create_usuario(db=db, usuario_data=usuario_data)
    
    # Construir respuesta con rol
    return {
        "id": usuario.id,
        "nombres": usuario.nombres,
        "apellido_paterno": usuario.apellido_paterno,
        "apellido_materno": usuario.apellido_materno,
        "email": usuario.email,
        "telefono": usuario.telefono,
        "rol_id": usuario.rol_id,
        "activo": usuario.activo,
        "fecha_registro": usuario.fecha_registro,
        "ultimo_login": usuario.ultimo_login,
        "rol_nombre": usuario.rol.nombre if usuario.rol else None,
    }


@router.get("/usuarios/{usuario_id}", response_model=UsuarioWithRol)
async def obtener_usuario(
    usuario_id: int,
    db: Session = Depends(get_db),
    _: None = Depends(require_permissions("usuarios:ver")),
):
    """
    Obtener usuario por ID.
    
    **Permisos requeridos:** `usuarios:ver`
    """
    usuario = usuario_service.get_usuario_by_id(db=db, usuario_id=usuario_id)
    
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Usuario con ID {usuario_id} no encontrado",
        )
    
    return {
        "id": usuario.id,
        "nombres": usuario.nombres,
        "apellido_paterno": usuario.apellido_paterno,
        "apellido_materno": usuario.apellido_materno,
        "email": usuario.email,
        "telefono": usuario.telefono,
        "rol_id": usuario.rol_id,
        "activo": usuario.activo,
        "fecha_registro": usuario.fecha_registro,
        "ultimo_login": usuario.ultimo_login,
        "rol_nombre": usuario.rol.nombre if usuario.rol else None,
    }


@router.put("/usuarios/{usuario_id}", response_model=UsuarioWithRol)
async def actualizar_usuario(
    usuario_id: int,
    usuario_data: UsuarioUpdate,
    db: Session = Depends(get_db),
    _: None = Depends(require_permissions("usuarios:editar")),
):
    """
    Actualizar datos de usuario existente.
    
    **Permisos requeridos:** `usuarios:editar`
    
    **Nota:** Solo se actualizan los campos enviados (PATCH semantics)
    """
    usuario = usuario_service.update_usuario(
        db=db,
        usuario_id=usuario_id,
        usuario_data=usuario_data,
    )
    
    return {
        "id": usuario.id,
        "nombres": usuario.nombres,
        "apellido_paterno": usuario.apellido_paterno,
        "apellido_materno": usuario.apellido_materno,
        "email": usuario.email,
        "telefono": usuario.telefono,
        "rol_id": usuario.rol_id,
        "activo": usuario.activo,
        "fecha_registro": usuario.fecha_registro,
        "ultimo_login": usuario.ultimo_login,
        "rol_nombre": usuario.rol.nombre if usuario.rol else None,
    }


@router.delete("/usuarios/{usuario_id}", status_code=status.HTTP_204_NO_CONTENT)
async def eliminar_usuario(
    usuario_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_active_user),
    _: None = Depends(require_permissions("usuarios:eliminar")),
):
    """
    Eliminar usuario (soft delete - marca como inactivo).
    
    **Permisos requeridos:** `usuarios:eliminar`
    
    **Nota:** No se puede eliminar a sí mismo
    """
    # Validar que no se está eliminando a sí mismo
    if usuario_id == current_user.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No puedes eliminarte a ti mismo",
        )
    
    usuario_service.delete_usuario(db=db, usuario_id=usuario_id)
    
    return None


@router.patch("/usuarios/{usuario_id}/toggle-activo", response_model=UsuarioWithRol)
async def toggle_activo_usuario(
    usuario_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_active_user),
    _: None = Depends(require_permissions("usuarios:editar")),
):
    """
    Activar/desactivar usuario.
    
    **Permisos requeridos:** `usuarios:editar`
    
    **Nota:** No se puede desactivar a sí mismo
    """
    # Validar que no se está desactivando a sí mismo
    if usuario_id == current_user.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No puedes desactivarte a ti mismo",
        )
    
    usuario = usuario_service.toggle_usuario_activo(db=db, usuario_id=usuario_id)
    
    return {
        "id": usuario.id,
        "nombres": usuario.nombres,
        "apellido_paterno": usuario.apellido_paterno,
        "apellido_materno": usuario.apellido_materno,
        "email": usuario.email,
        "telefono": usuario.telefono,
        "rol_id": usuario.rol_id,
        "activo": usuario.activo,
        "fecha_registro": usuario.fecha_registro,
        "ultimo_login": usuario.ultimo_login,
        "rol_nombre": usuario.rol.nombre if usuario.rol else None,
    }
