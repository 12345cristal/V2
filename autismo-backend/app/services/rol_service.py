"""
Rol Service - Lógica de negocio para gestión de roles y permisos
"""

from typing import Optional, List
from sqlalchemy.orm import Session, joinedload
from fastapi import HTTPException, status

from app.models.rol import Rol
from app.models.permiso import Permiso
from app.models.role_permiso import RolePermiso
from app.schemas.rol import RolCreate, RolUpdate


def get_roles(db: Session) -> List[Rol]:
    """
    Obtener lista de todos los roles
    
    Args:
        db: Session de base de datos
    
    Returns:
        Lista de roles
    """
    return db.query(Rol).order_by(Rol.id).all()


def get_rol_by_id(db: Session, rol_id: int) -> Optional[Rol]:
    """
    Obtener rol por ID
    
    Args:
        db: Session de base de datos
        rol_id: ID del rol
    
    Returns:
        Rol o None si no existe
    """
    return db.query(Rol).filter(Rol.id == rol_id).first()


def get_rol_with_permisos(db: Session, rol_id: int) -> Optional[dict]:
    """
    Obtener rol con sus permisos
    
    Args:
        db: Session de base de datos
        rol_id: ID del rol
    
    Returns:
        Diccionario con datos del rol y lista de permisos
    
    Raises:
        HTTPException: Si el rol no existe
    """
    rol = get_rol_by_id(db, rol_id)
    if not rol:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Rol con ID {rol_id} no encontrado",
        )
    
    # Obtener permisos del rol
    permisos = (
        db.query(Permiso)
        .join(RolePermiso, RolePermiso.permiso_id == Permiso.id)
        .filter(RolePermiso.role_id == rol_id)
        .all()
    )
    
    return {
        "id": rol.id,
        "nombre": rol.nombre,
        "descripcion": rol.descripcion,
        "permisos": permisos,
    }


def get_all_permisos(db: Session) -> List[Permiso]:
    """
    Obtener lista de todos los permisos disponibles
    
    Args:
        db: Session de base de datos
    
    Returns:
        Lista de permisos
    """
    return db.query(Permiso).order_by(Permiso.codigo).all()


def create_rol(db: Session, rol_data: RolCreate) -> Rol:
    """
    Crear nuevo rol
    
    Args:
        db: Session de base de datos
        rol_data: Datos del rol a crear
    
    Returns:
        Rol creado
    
    Raises:
        HTTPException: Si el nombre del rol ya existe
    """
    # Verificar que el nombre no exista
    existing_rol = db.query(Rol).filter(Rol.nombre == rol_data.nombre).first()
    if existing_rol:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Ya existe un rol con el nombre '{rol_data.nombre}'",
        )
    
    db_rol = Rol(
        nombre=rol_data.nombre,
        descripcion=rol_data.descripcion,
    )
    
    db.add(db_rol)
    db.commit()
    db.refresh(db_rol)
    
    return db_rol


def update_rol(db: Session, rol_id: int, rol_data: RolUpdate) -> Rol:
    """
    Actualizar rol existente
    
    Args:
        db: Session de base de datos
        rol_id: ID del rol a actualizar
        rol_data: Datos a actualizar
    
    Returns:
        Rol actualizado
    
    Raises:
        HTTPException: Si el rol no existe o el nombre ya está en uso
    """
    db_rol = get_rol_by_id(db, rol_id)
    if not db_rol:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Rol con ID {rol_id} no encontrado",
        )
    
    # Si se está actualizando el nombre, verificar que no exista
    if rol_data.nombre and rol_data.nombre != db_rol.nombre:
        existing_rol = db.query(Rol).filter(Rol.nombre == rol_data.nombre).first()
        if existing_rol:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Ya existe un rol con el nombre '{rol_data.nombre}'",
            )
    
    # Actualizar campos
    update_data = rol_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_rol, field, value)
    
    db.commit()
    db.refresh(db_rol)
    
    return db_rol


def assign_permisos_to_rol(
    db: Session,
    rol_id: int,
    permiso_ids: List[int],
) -> dict:
    """
    Asignar permisos a un rol (reemplaza los permisos existentes)
    
    Args:
        db: Session de base de datos
        rol_id: ID del rol
        permiso_ids: Lista de IDs de permisos a asignar
    
    Returns:
        Diccionario con rol y permisos asignados
    
    Raises:
        HTTPException: Si el rol no existe o algún permiso no existe
    """
    # Verificar que el rol exista
    rol = get_rol_by_id(db, rol_id)
    if not rol:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Rol con ID {rol_id} no encontrado",
        )
    
    # Verificar que todos los permisos existan
    permisos = db.query(Permiso).filter(Permiso.id.in_(permiso_ids)).all()
    if len(permisos) != len(permiso_ids):
        permisos_encontrados = {p.id for p in permisos}
        permisos_invalidos = set(permiso_ids) - permisos_encontrados
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Permisos no encontrados: {permisos_invalidos}",
        )
    
    # Eliminar permisos existentes del rol
    db.query(RolePermiso).filter(RolePermiso.role_id == rol_id).delete()
    
    # Asignar nuevos permisos
    for permiso_id in permiso_ids:
        role_permiso = RolePermiso(role_id=rol_id, permiso_id=permiso_id)
        db.add(role_permiso)
    
    db.commit()
    
    # Retornar rol con permisos
    return get_rol_with_permisos(db, rol_id)


def get_permisos_by_rol_id(db: Session, rol_id: int) -> List[Permiso]:
    """
    Obtener permisos de un rol específico
    
    Args:
        db: Session de base de datos
        rol_id: ID del rol
    
    Returns:
        Lista de permisos del rol
    """
    return (
        db.query(Permiso)
        .join(RolePermiso, RolePermiso.permiso_id == Permiso.id)
        .filter(RolePermiso.role_id == rol_id)
        .order_by(Permiso.codigo)
        .all()
    )


def create_permiso(db: Session, codigo: str, descripcion: Optional[str] = None) -> Permiso:
    """
    Crear nuevo permiso
    
    Args:
        db: Session de base de datos
        codigo: Código del permiso (ej: "usuarios:ver")
        descripcion: Descripción del permiso
    
    Returns:
        Permiso creado
    
    Raises:
        HTTPException: Si el código ya existe
    """
    existing_permiso = db.query(Permiso).filter(Permiso.codigo == codigo).first()
    if existing_permiso:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Ya existe un permiso con el código '{codigo}'",
        )
    
    db_permiso = Permiso(codigo=codigo, descripcion=descripcion)
    db.add(db_permiso)
    db.commit()
    db.refresh(db_permiso)
    
    return db_permiso
