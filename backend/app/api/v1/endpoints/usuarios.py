# app/api/v1/endpoints/usuarios.py

from fastapi import APIRouter, Depends
from typing import List
from sqlalchemy.orm import Session

from app.api.deps import get_db, require_permissions
from app.schemas.usuario import (
    UsuarioCreate, UsuarioUpdate, UsuarioRead,
    UsuarioEstadoUpdate, UsuarioPasswordUpdate
)
from app.services.usuario_service import (
    listar_usuarios, crear_usuario, actualizar_usuario,
    cambiar_estado, cambiar_password, personal_sin_usuario
)
from app.schemas.personal import PersonalRead

router = APIRouter(prefix="/usuarios", tags=["Usuarios"])


# ======================================================
# LISTADO DE USUARIOS
# ======================================================
@router.get("", response_model=List[UsuarioRead])
def get_usuarios(
    db: Session = Depends(get_db),
    _=Depends(require_permissions(["USUARIOS_VER"]))
):
    return listar_usuarios(db)


# ======================================================
# CREAR USUARIO
# ======================================================
@router.post("", response_model=UsuarioRead)
def post_usuario(
    data: UsuarioCreate,
    db: Session = Depends(get_db),
    _=Depends(require_permissions(["USUARIOS_CREAR"]))
):
    return crear_usuario(db, data)


# ======================================================
# ACTUALIZAR USUARIO
# ======================================================
@router.put("/{id_usuario}", response_model=UsuarioRead)
def put_usuario(
    id_usuario: int,
    data: UsuarioUpdate,
    db: Session = Depends(get_db),
    _=Depends(require_permissions(["USUARIOS_EDITAR"]))
):
    return actualizar_usuario(db, id_usuario, data)


# ======================================================
# CAMBIAR ESTADO (ACTIVO / INACTIVO / BLOQUEADO)
# ======================================================
@router.patch("/{id_usuario}/estado", response_model=UsuarioRead)
def patch_estado_usuario(
    id_usuario: int,
    data: UsuarioEstadoUpdate,
    db: Session = Depends(get_db),
    _=Depends(require_permissions(["USUARIOS_EDITAR"]))
):
    return cambiar_estado(db, id_usuario, data.estado)


# ======================================================
# CAMBIAR PASSWORD
# ======================================================
@router.patch("/{id_usuario}/password")
def patch_password_usuario(
    id_usuario: int,
    data: UsuarioPasswordUpdate,
    db: Session = Depends(get_db),
    _=Depends(require_permissions(["USUARIOS_EDITAR"]))
):
    return cambiar_password(db, id_usuario, data)


# ======================================================
# PERSONAL SIN USUARIO
# ======================================================
@router.get("/personal/sin-usuario", response_model=List[PersonalRead])
def get_personal_sin_usuario(
    db: Session = Depends(get_db),
    _=Depends(require_permissions(["USUARIOS_CREAR"]))
):
    return personal_sin_usuario(db)
