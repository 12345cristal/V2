"""
Personal Service - Lógica de negocio para gestión de personal (terapeutas)
"""

from typing import Optional, List
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import or_
from fastapi import HTTPException, status

from app.models.personal import Personal, PersonalPerfil, PersonalHorario
from app.models.usuario import Usuario
from app.schemas.personal import (
    PersonalCreate,
    PersonalUpdate,
    PersonalPerfilCreate,
    PersonalPerfilUpdate,
    PersonalHorarioCreate,
    PersonalHorarioUpdate,
)


def get_personal_list(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    search: Optional[str] = None,
    especialidad: Optional[str] = None,
    estatus: Optional[str] = None,
) -> List[Personal]:
    """
    Obtener lista de personal con filtros opcionales
    
    Args:
        db: Session de base de datos
        skip: Número de registros a saltar
        limit: Número máximo de registros
        search: Búsqueda por nombre
        especialidad: Filtrar por especialidad
        estatus: Filtrar por estatus (ACTIVO, INACTIVO, LICENCIA)
    
    Returns:
        Lista de personal
    """
    query = db.query(Personal).options(
        joinedload(Personal.usuario),
        joinedload(Personal.perfil),
    )
    
    # Aplicar filtros
    if search:
        search_filter = f"%{search}%"
        query = query.join(Usuario).filter(
            or_(
                Usuario.nombres.ilike(search_filter),
                Usuario.apellido_paterno.ilike(search_filter),
                Usuario.apellido_materno.ilike(search_filter),
            )
        )
    
    if especialidad:
        query = query.filter(Personal.especialidad.ilike(f"%{especialidad}%"))
    
    if estatus:
        query = query.filter(Personal.estatus == estatus)
    
    return query.offset(skip).limit(limit).all()


def get_personal_by_id(db: Session, personal_id: int) -> Optional[Personal]:
    """
    Obtener personal por ID con relaciones cargadas
    
    Args:
        db: Session de base de datos
        personal_id: ID del personal
    
    Returns:
        Personal o None si no existe
    """
    return (
        db.query(Personal)
        .options(
            joinedload(Personal.usuario),
            joinedload(Personal.perfil),
            joinedload(Personal.horarios),
        )
        .filter(Personal.id == personal_id)
        .first()
    )


def get_personal_by_usuario_id(db: Session, usuario_id: int) -> Optional[Personal]:
    """
    Obtener personal por ID de usuario
    
    Args:
        db: Session de base de datos
        usuario_id: ID del usuario
    
    Returns:
        Personal o None si no existe
    """
    return (
        db.query(Personal)
        .options(joinedload(Personal.usuario))
        .filter(Personal.usuario_id == usuario_id)
        .first()
    )


def create_personal(db: Session, personal_data: PersonalCreate) -> Personal:
    """
    Crear nuevo personal
    
    Args:
        db: Session de base de datos
        personal_data: Datos del personal a crear
    
    Returns:
        Personal creado
    
    Raises:
        HTTPException: Si el usuario no existe o ya es personal
    """
    # Validar que el usuario exista
    usuario = db.query(Usuario).filter(Usuario.id == personal_data.usuario_id).first()
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Usuario con ID {personal_data.usuario_id} no encontrado",
        )
    
    # Validar que el usuario no sea ya personal
    existing_personal = get_personal_by_usuario_id(db, personal_data.usuario_id)
    if existing_personal:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"El usuario ya está registrado como personal",
        )
    
    # Crear personal
    db_personal = Personal(
        usuario_id=personal_data.usuario_id,
        especialidad=personal_data.especialidad,
        certificaciones=personal_data.certificaciones,
        anos_experiencia=personal_data.anos_experiencia,
        numero_licencia=personal_data.numero_licencia,
        estatus=personal_data.estatus or "ACTIVO",
    )
    
    db.add(db_personal)
    db.commit()
    db.refresh(db_personal)
    
    return db_personal


def update_personal(
    db: Session,
    personal_id: int,
    personal_data: PersonalUpdate,
) -> Personal:
    """
    Actualizar datos de personal existente
    
    Args:
        db: Session de base de datos
        personal_id: ID del personal a actualizar
        personal_data: Datos a actualizar
    
    Returns:
        Personal actualizado
    
    Raises:
        HTTPException: Si el personal no existe
    """
    db_personal = get_personal_by_id(db, personal_id)
    if not db_personal:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Personal con ID {personal_id} no encontrado",
        )
    
    # Actualizar campos que no sean None
    update_data = personal_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_personal, field, value)
    
    db.commit()
    db.refresh(db_personal)
    
    return db_personal


def delete_personal(db: Session, personal_id: int) -> bool:
    """
    Eliminar personal (marcar como INACTIVO)
    
    Args:
        db: Session de base de datos
        personal_id: ID del personal a eliminar
    
    Returns:
        True si se eliminó correctamente
    
    Raises:
        HTTPException: Si el personal no existe
    """
    db_personal = get_personal_by_id(db, personal_id)
    if not db_personal:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Personal con ID {personal_id} no encontrado",
        )
    
    # Soft delete: cambiar estatus a INACTIVO
    db_personal.estatus = "INACTIVO"
    db.commit()
    
    return True


# ============= PERFIL FUNCTIONS =============

def create_perfil(
    db: Session,
    personal_id: int,
    perfil_data: PersonalPerfilCreate,
) -> PersonalPerfil:
    """
    Crear perfil de personal
    
    Args:
        db: Session de base de datos
        personal_id: ID del personal
        perfil_data: Datos del perfil
    
    Returns:
        Perfil creado
    
    Raises:
        HTTPException: Si el personal no existe o ya tiene perfil
    """
    # Validar que el personal exista
    personal = get_personal_by_id(db, personal_id)
    if not personal:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Personal con ID {personal_id} no encontrado",
        )
    
    # Validar que no tenga perfil
    if personal.perfil:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El personal ya tiene un perfil registrado",
        )
    
    db_perfil = PersonalPerfil(
        personal_id=personal_id,
        fecha_nacimiento=perfil_data.fecha_nacimiento,
        direccion=perfil_data.direccion,
        ciudad=perfil_data.ciudad,
        estado=perfil_data.estado,
        codigo_postal=perfil_data.codigo_postal,
        grado_academico_id=perfil_data.grado_academico_id,
        estado_laboral_id=perfil_data.estado_laboral_id,
        fecha_contratacion=perfil_data.fecha_contratacion,
    )
    
    db.add(db_perfil)
    db.commit()
    db.refresh(db_perfil)
    
    return db_perfil


def update_perfil(
    db: Session,
    personal_id: int,
    perfil_data: PersonalPerfilUpdate,
) -> PersonalPerfil:
    """
    Actualizar perfil de personal
    
    Args:
        db: Session de base de datos
        personal_id: ID del personal
        perfil_data: Datos a actualizar
    
    Returns:
        Perfil actualizado
    
    Raises:
        HTTPException: Si el personal o perfil no existe
    """
    personal = get_personal_by_id(db, personal_id)
    if not personal:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Personal con ID {personal_id} no encontrado",
        )
    
    if not personal.perfil:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="El personal no tiene perfil registrado",
        )
    
    # Actualizar campos
    update_data = perfil_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(personal.perfil, field, value)
    
    db.commit()
    db.refresh(personal.perfil)
    
    return personal.perfil


# ============= HORARIO FUNCTIONS =============

def get_horarios_by_personal(db: Session, personal_id: int) -> List[PersonalHorario]:
    """
    Obtener horarios de un personal
    
    Args:
        db: Session de base de datos
        personal_id: ID del personal
    
    Returns:
        Lista de horarios
    """
    return (
        db.query(PersonalHorario)
        .filter(PersonalHorario.personal_id == personal_id)
        .order_by(PersonalHorario.dia_semana, PersonalHorario.hora_inicio)
        .all()
    )


def create_horario(
    db: Session,
    horario_data: PersonalHorarioCreate,
) -> PersonalHorario:
    """
    Crear horario de personal
    
    Args:
        db: Session de base de datos
        horario_data: Datos del horario
    
    Returns:
        Horario creado
    
    Raises:
        HTTPException: Si el personal no existe
    """
    # Validar que el personal exista
    personal = get_personal_by_id(db, horario_data.personal_id)
    if not personal:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Personal con ID {horario_data.personal_id} no encontrado",
        )
    
    db_horario = PersonalHorario(
        personal_id=horario_data.personal_id,
        dia_semana=horario_data.dia_semana,
        hora_inicio=horario_data.hora_inicio,
        hora_fin=horario_data.hora_fin,
    )
    
    db.add(db_horario)
    db.commit()
    db.refresh(db_horario)
    
    return db_horario


def update_horario(
    db: Session,
    horario_id: int,
    horario_data: PersonalHorarioUpdate,
) -> PersonalHorario:
    """
    Actualizar horario de personal
    
    Args:
        db: Session de base de datos
        horario_id: ID del horario
        horario_data: Datos a actualizar
    
    Returns:
        Horario actualizado
    
    Raises:
        HTTPException: Si el horario no existe
    """
    db_horario = db.query(PersonalHorario).filter(PersonalHorario.id == horario_id).first()
    if not db_horario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Horario con ID {horario_id} no encontrado",
        )
    
    # Actualizar campos
    update_data = horario_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_horario, field, value)
    
    db.commit()
    db.refresh(db_horario)
    
    return db_horario


def delete_horario(db: Session, horario_id: int) -> bool:
    """
    Eliminar horario de personal
    
    Args:
        db: Session de base de datos
        horario_id: ID del horario
    
    Returns:
        True si se eliminó correctamente
    
    Raises:
        HTTPException: Si el horario no existe
    """
    db_horario = db.query(PersonalHorario).filter(PersonalHorario.id == horario_id).first()
    if not db_horario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Horario con ID {horario_id} no encontrado",
        )
    
    db.delete(db_horario)
    db.commit()
    
    return True


def count_personal(
    db: Session,
    search: Optional[str] = None,
    especialidad: Optional[str] = None,
    estatus: Optional[str] = None,
) -> int:
    """
    Contar personal con filtros opcionales
    
    Args:
        db: Session de base de datos
        search: Búsqueda por nombre
        especialidad: Filtrar por especialidad
        estatus: Filtrar por estatus
    
    Returns:
        Número total de personal
    """
    query = db.query(Personal)
    
    if search:
        search_filter = f"%{search}%"
        query = query.join(Usuario).filter(
            or_(
                Usuario.nombres.ilike(search_filter),
                Usuario.apellido_paterno.ilike(search_filter),
                Usuario.apellido_materno.ilike(search_filter),
            )
        )
    
    if especialidad:
        query = query.filter(Personal.especialidad.ilike(f"%{especialidad}%"))
    
    if estatus:
        query = query.filter(Personal.estatus == estatus)
    
    return query.count()
