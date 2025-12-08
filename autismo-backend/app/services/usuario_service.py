"""
Usuario Service - Lógica de negocio para gestión de usuarios
"""

from typing import Optional, List
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import or_
from fastapi import HTTPException, status

from app.models.usuario import Usuario
from app.models.rol import Rol
from app.schemas.usuario import UsuarioCreate, UsuarioUpdate
from app.core.security import hash_password


def get_usuarios(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    search: Optional[str] = None,
    rol_id: Optional[int] = None,
    activo: Optional[int] = None,
) -> List[Usuario]:
    """
    Obtener lista de usuarios con filtros opcionales
    
    Args:
        db: Session de base de datos
        skip: Número de registros a saltar (paginación)
        limit: Número máximo de registros
        search: Búsqueda por nombre o email
        rol_id: Filtrar por rol
        activo: Filtrar por estado activo (0 o 1)
    
    Returns:
        Lista de usuarios
    """
    query = db.query(Usuario).options(joinedload(Usuario.rol))
    
    # Aplicar filtros
    if search:
        search_filter = f"%{search}%"
        query = query.filter(
            or_(
                Usuario.nombres.ilike(search_filter),
                Usuario.apellido_paterno.ilike(search_filter),
                Usuario.apellido_materno.ilike(search_filter),
                Usuario.email.ilike(search_filter),
            )
        )
    
    if rol_id is not None:
        query = query.filter(Usuario.rol_id == rol_id)
    
    if activo is not None:
        query = query.filter(Usuario.activo == activo)
    
    # Ordenar por fecha de registro descendente
    query = query.order_by(Usuario.fecha_registro.desc())
    
    return query.offset(skip).limit(limit).all()


def get_usuario_by_id(db: Session, usuario_id: int) -> Optional[Usuario]:
    """
    Obtener usuario por ID con su rol cargado
    
    Args:
        db: Session de base de datos
        usuario_id: ID del usuario
    
    Returns:
        Usuario o None si no existe
    """
    return (
        db.query(Usuario)
        .options(joinedload(Usuario.rol))
        .filter(Usuario.id == usuario_id)
        .first()
    )


def get_usuario_by_email(db: Session, email: str) -> Optional[Usuario]:
    """
    Obtener usuario por email
    
    Args:
        db: Session de base de datos
        email: Email del usuario
    
    Returns:
        Usuario o None si no existe
    """
    return db.query(Usuario).filter(Usuario.email == email).first()


def create_usuario(db: Session, usuario_data: UsuarioCreate) -> Usuario:
    """
    Crear nuevo usuario
    
    Args:
        db: Session de base de datos
        usuario_data: Datos del usuario a crear
    
    Returns:
        Usuario creado
    
    Raises:
        HTTPException: Si el email ya existe o el rol no es válido
    """
    # Validar que el email no exista
    existing_user = get_usuario_by_email(db, usuario_data.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"El email {usuario_data.email} ya está registrado",
        )
    
    # Validar que el rol exista
    rol = db.query(Rol).filter(Rol.id == usuario_data.rol_id).first()
    if not rol:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"El rol con ID {usuario_data.rol_id} no existe",
        )
    
    # Crear usuario
    db_usuario = Usuario(
        nombres=usuario_data.nombres,
        apellido_paterno=usuario_data.apellido_paterno,
        apellido_materno=usuario_data.apellido_materno,
        email=usuario_data.email,
        telefono=usuario_data.telefono,
        hashed_password=hash_password(usuario_data.password),
        rol_id=usuario_data.rol_id,
        activo=1,  # Activo por defecto
    )
    
    db.add(db_usuario)
    db.commit()
    db.refresh(db_usuario)
    
    return db_usuario


def update_usuario(
    db: Session,
    usuario_id: int,
    usuario_data: UsuarioUpdate,
) -> Usuario:
    """
    Actualizar datos de usuario existente
    
    Args:
        db: Session de base de datos
        usuario_id: ID del usuario a actualizar
        usuario_data: Datos a actualizar
    
    Returns:
        Usuario actualizado
    
    Raises:
        HTTPException: Si el usuario no existe o el email ya está en uso
    """
    db_usuario = get_usuario_by_id(db, usuario_id)
    if not db_usuario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Usuario con ID {usuario_id} no encontrado",
        )
    
    # Si se está actualizando el email, verificar que no exista
    if usuario_data.email and usuario_data.email != db_usuario.email:
        existing_user = get_usuario_by_email(db, usuario_data.email)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"El email {usuario_data.email} ya está registrado",
            )
    
    # Si se está actualizando el rol, validar que exista
    if usuario_data.rol_id:
        rol = db.query(Rol).filter(Rol.id == usuario_data.rol_id).first()
        if not rol:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"El rol con ID {usuario_data.rol_id} no existe",
            )
    
    # Actualizar campos que no sean None
    update_data = usuario_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_usuario, field, value)
    
    db.commit()
    db.refresh(db_usuario)
    
    return db_usuario


def delete_usuario(db: Session, usuario_id: int) -> bool:
    """
    Eliminar usuario (soft delete - marcar como inactivo)
    
    Args:
        db: Session de base de datos
        usuario_id: ID del usuario a eliminar
    
    Returns:
        True si se eliminó correctamente
    
    Raises:
        HTTPException: Si el usuario no existe
    """
    db_usuario = get_usuario_by_id(db, usuario_id)
    if not db_usuario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Usuario con ID {usuario_id} no encontrado",
        )
    
    # Soft delete: marcar como inactivo
    db_usuario.activo = 0
    db.commit()
    
    return True


def toggle_usuario_activo(db: Session, usuario_id: int) -> Usuario:
    """
    Activar/desactivar usuario
    
    Args:
        db: Session de base de datos
        usuario_id: ID del usuario
    
    Returns:
        Usuario actualizado
    
    Raises:
        HTTPException: Si el usuario no existe
    """
    db_usuario = get_usuario_by_id(db, usuario_id)
    if not db_usuario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Usuario con ID {usuario_id} no encontrado",
        )
    
    # Toggle activo
    db_usuario.activo = 1 if db_usuario.activo == 0 else 0
    db.commit()
    db.refresh(db_usuario)
    
    return db_usuario


def count_usuarios(
    db: Session,
    search: Optional[str] = None,
    rol_id: Optional[int] = None,
    activo: Optional[int] = None,
) -> int:
    """
    Contar usuarios con filtros opcionales
    
    Args:
        db: Session de base de datos
        search: Búsqueda por nombre o email
        rol_id: Filtrar por rol
        activo: Filtrar por estado activo
    
    Returns:
        Número total de usuarios que cumplen los filtros
    """
    query = db.query(Usuario)
    
    if search:
        search_filter = f"%{search}%"
        query = query.filter(
            or_(
                Usuario.nombres.ilike(search_filter),
                Usuario.apellido_paterno.ilike(search_filter),
                Usuario.apellido_materno.ilike(search_filter),
                Usuario.email.ilike(search_filter),
            )
        )
    
    if rol_id is not None:
        query = query.filter(Usuario.rol_id == rol_id)
    
    if activo is not None:
        query = query.filter(Usuario.activo == activo)
    
    return query.count()
