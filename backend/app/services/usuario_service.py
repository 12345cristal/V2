# app/services/usuario_service.py

from typing import List
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.models.usuario import Usuario, EstadoUsuarioEnum
from app.models.personal import Personal
from app.schemas.usuario import (
    UsuarioCreate,
    UsuarioUpdate,
    UsuarioEstadoUpdate,
    UsuarioPasswordUpdate,
    UsuarioListado,
)
from app.core.security import get_password_hash


# =============================================================
# LISTAR USUARIOS
# =============================================================
def list_usuarios(db: Session) -> List[UsuarioListado]:
    """
    Obtiene todos los usuarios junto con información del personal asociado.
    """
    query = db.query(Usuario, Personal).join(Personal, Usuario.id_personal == Personal.id_personal)
    resultado = []

    for usuario, personal in query.all():
        resultado.append(
            UsuarioListado(
                id_usuario=usuario.id_usuario,
                id_personal=usuario.id_personal,
                username=usuario.username,
                rol_sistema=usuario.rol_sistema,
                estado=usuario.estado,
                debe_cambiar_password=usuario.debe_cambiar_password,
                fecha_creacion=usuario.fecha_creacion.isoformat() if usuario.fecha_creacion else None,
                ultima_sesion=usuario.ultima_sesion.isoformat() if usuario.ultima_sesion else None,
                nombre_completo=f"{personal.nombres} {personal.apellido_paterno} {personal.apellido_materno or ''}".strip(),
                nombre_rol_personal=personal.especialidad_principal,
                estado_laboral=personal.estado_laboral.value if personal.estado_laboral else None,
            )
        )
    return resultado


# =============================================================
# CREAR USUARIO
# =============================================================
def create_usuario(db: Session, obj_in: UsuarioCreate) -> Usuario:
    """
    Crea un nuevo usuario validando duplicados y asociando con un personal existente.
    """
    # Validar personal
    personal = db.query(Personal).get(obj_in.id_personal)
    if not personal:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Personal no encontrado")

    # Validar username duplicado
    if db.query(Usuario).filter(Usuario.username == obj_in.username).first():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username ya en uso")

    # Validar que el personal no tenga otro usuario
    if db.query(Usuario).filter(Usuario.id_personal == obj_in.id_personal).first():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Ese personal ya tiene un usuario asignado")

    # Crear usuario
    usuario = Usuario(
        id_personal=obj_in.id_personal,
        username=obj_in.username,
        rol_sistema=obj_in.rol_sistema,
        hashed_password=get_password_hash(obj_in.password),
        estado=EstadoUsuarioEnum.ACTIVO,
        debe_cambiar_password=obj_in.debe_cambiar_password,
    )
    db.add(usuario)
    db.commit()
    db.refresh(usuario)
    return usuario


# =============================================================
# OBTENER USUARIO POR ID
# =============================================================
def get_usuario(db: Session, id_usuario: int) -> Usuario:
    usuario = db.query(Usuario).get(id_usuario)
    if not usuario:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado")
    return usuario


# =============================================================
# ACTUALIZAR USUARIO
# =============================================================
def update_usuario(db: Session, id_usuario: int, obj_in: UsuarioUpdate) -> Usuario:
    """
    Actualiza campos de un usuario existente.
    """
    usuario = get_usuario(db, id_usuario)

    # Validar username si se intenta cambiar
    if obj_in.username and obj_in.username != usuario.username:
        if db.query(Usuario).filter(Usuario.username == obj_in.username).first():
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username ya en uso")

    data = obj_in.model_dump(exclude_unset=True)
    for field, value in data.items():
        setattr(usuario, field, value)

    db.add(usuario)
    db.commit()
    db.refresh(usuario)
    return usuario


# =============================================================
# CAMBIAR ESTADO DE USUARIO
# =============================================================
def cambiar_estado_usuario(db: Session, id_usuario: int, obj_in: UsuarioEstadoUpdate) -> Usuario:
    """
    Cambia el estado de un usuario (ACTIVO, INACTIVO, BLOQUEADO).
    """
    usuario = get_usuario(db, id_usuario)
    usuario.estado = obj_in.estado
    db.add(usuario)
    db.commit()
    db.refresh(usuario)
    return usuario


# =============================================================
# CAMBIAR PASSWORD
# =============================================================
def cambiar_password(db: Session, id_usuario: int, obj_in: UsuarioPasswordUpdate) -> None:
    """
    Actualiza la contraseña de un usuario y su flag de cambio obligatorio.
    """
    usuario = get_usuario(db, id_usuario)
    usuario.hashed_password = get_password_hash(obj_in.password)
    usuario.debe_cambiar_password = obj_in.debe_cambiar_password
    db.add(usuario)
    db.commit()


# =============================================================
# LISTAR PERSONAL SIN USUARIO
# =============================================================
def personal_sin_usuario(db: Session) -> List[Personal]:
    """
    Devuelve el personal que aún no tiene usuario asignado.
    """
    usuarios_existentes = {u.id_personal for u in db.query(Usuario).all()}
    return db.query(Personal).filter(~Personal.id_personal.in_(usuarios_existentes)).all()
