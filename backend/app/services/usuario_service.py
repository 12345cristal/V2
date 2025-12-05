# app/services/usuario_service.py

from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.core.security import get_password_hash
from app.models.usuario import Usuario
from app.models.personal import Personal
from app.models.rol import Rol
from app.schemas.usuario import (
    UsuarioCreate, UsuarioUpdate, UsuarioPasswordUpdate
)


def listar_usuarios(db: Session):
    usuarios = db.query(Usuario).all()
    resultado = []

    for u in usuarios:
        personal = db.query(Personal).filter(Personal.id_personal == u.id_personal).first()
        nombre_completo = f"{personal.nombres} {personal.apellido_paterno}" if personal else None

        resultado.append({
            "id_usuario": u.id_usuario,
            "id_personal": u.id_personal,
            "username": u.username,
            "email": u.email,
            "rol_sistema": u.rol_sistema,
            "estado": u.estado,
            "debe_cambiar_password": u.debe_cambiar_password,
            "fecha_creacion": u.fecha_creacion,
            "ultima_sesion": u.ultima_sesion,
            "nombre_completo": nombre_completo,
            "nombre_rol_personal": personal.especialidad_principal if personal else None,
            "estado_laboral": personal.estado_laboral if personal else None
        })
    return resultado


def crear_usuario(db: Session, data: UsuarioCreate):
    # validar duplicados
    if db.query(Usuario).filter(Usuario.username == data.username).first():
        raise HTTPException(400, "El username ya está en uso")

    if db.query(Usuario).filter(Usuario.email == data.email).first():
        raise HTTPException(400, "El email ya está registrado")

    # validar que el personal no tenga usuario
    if db.query(Usuario).filter(Usuario.id_personal == data.id_personal).first():
        raise HTTPException(400, "Este personal ya tiene un usuario asignado")

    hashed = get_password_hash(data.password)

    usuario = Usuario(
        id_personal=data.id_personal,
        username=data.username,
        email=data.email,
        hashed_password=hashed,
        rol_sistema=data.rol_sistema,
        estado=data.estado,
        debe_cambiar_password=data.debe_cambiar_password
    )

    db.add(usuario)
    db.commit()
    db.refresh(usuario)
    return usuario


def actualizar_usuario(db: Session, id_usuario: int, data: UsuarioUpdate):
    usuario = db.query(Usuario).filter(Usuario.id_usuario == id_usuario).first()
    if not usuario:
        raise HTTPException(404, "Usuario no encontrado")

    # actualizar valores
    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(usuario, key, value)

    db.commit()
    db.refresh(usuario)
    return usuario


def cambiar_estado(db: Session, id_usuario: int, nuevo_estado: str):
    usuario = db.query(Usuario).filter(Usuario.id_usuario == id_usuario).first()
    if not usuario:
        raise HTTPException(404, "Usuario no encontrado")

    usuario.estado = nuevo_estado
    db.commit()
    db.refresh(usuario)
    return usuario


def cambiar_password(db: Session, id_usuario: int, data: UsuarioPasswordUpdate):
    usuario = db.query(Usuario).filter(Usuario.id_usuario == id_usuario).first()
    if not usuario:
        raise HTTPException(404, "Usuario no encontrado")

    usuario.hashed_password = get_password_hash(data.password)
    usuario.debe_cambiar_password = data.debe_cambiar_password

    db.commit()
    return {"ok": True}


def personal_sin_usuario(db: Session):
    """devuelve personal que NO tenga cuenta aún"""
    con_usuario = {u.id_personal for u in db.query(Usuario).all()}
    return db.query(Personal).filter(~Personal.id_personal.in_(con_usuario)).all()
