# app/api/v1/endpoints/usuarios.py

from typing import List
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.api.deps import get_db, get_current_active_user, require_permissions
from app.schemas.usuario import (
    UsuarioCreate,
    UsuarioUpdate,
    UsuarioRead,
    UsuarioListado,
    UsuarioEstadoUpdate,
    UsuarioPasswordUpdate,
)
from app.schemas.personal import PersonalRead
from app.services.usuario_service import (
    list_usuarios,
    create_usuario,
    update_usuario,
    cambiar_estado_usuario,
    cambiar_password,
    personal_sin_usuario,
)

router = APIRouter(
    prefix="/usuarios",
    tags=["usuarios"],
    dependencies=[Depends(get_current_active_user)],
)


# =============================================================
# LISTAR USUARIOS
# =============================================================
@router.get("", response_model=List[UsuarioListado])
def get_usuarios(
    db: Session = Depends(get_db),
    _: dict = Depends(require_permissions(["USUARIOS_VER"])),
):
    """
    Devuelve el listado completo de usuarios con información del personal asociado.
    """
    return list_usuarios(db)


# =============================================================
# CREAR USUARIO
# =============================================================
@router.post("", response_model=UsuarioRead, status_code=status.HTTP_201_CREATED)
def post_usuario(
    obj_in: UsuarioCreate,
    db: Session = Depends(get_db),
    _: dict = Depends(require_permissions(["USUARIOS_CREAR"])),
):
    """
    Crea un nuevo usuario validando duplicados y asociando un personal.
    """
    return create_usuario(db, obj_in)


# =============================================================
# ACTUALIZAR USUARIO
# =============================================================
@router.put("/{id_usuario}", response_model=UsuarioRead)
def put_usuario(
    id_usuario: int,
    obj_in: UsuarioUpdate,
    db: Session = Depends(get_db),
    _: dict = Depends(require_permissions(["USUARIOS_EDITAR"])),
):
    """
    Actualiza los datos generales de un usuario.
    """
    return update_usuario(db, id_usuario, obj_in)


# =============================================================
# CAMBIAR ESTADO (ACTIVO / INACTIVO / BLOQUEADO)
# =============================================================
@router.patch("/{id_usuario}/estado", response_model=UsuarioRead)
def patch_estado_usuario(
    id_usuario: int,
    obj_in: UsuarioEstadoUpdate,
    db: Session = Depends(get_db),
    _: dict = Depends(require_permissions(["USUARIOS_EDITAR"])),
):
    """
    Cambia el estado de un usuario.
    """
    return cambiar_estado_usuario(db, id_usuario, obj_in)


# =============================================================
# CAMBIAR PASSWORD
# =============================================================
@router.patch("/{id_usuario}/password", status_code=status.HTTP_204_NO_CONTENT)
def patch_password_usuario(
    id_usuario: int,
    obj_in: UsuarioPasswordUpdate,
    db: Session = Depends(get_db),
    _: dict = Depends(require_permissions(["USUARIOS_EDITAR"])),
):
    """
    Actualiza la contraseña de un usuario y su flag de cambio obligatorio.
    """
    cambiar_password(db, id_usuario, obj_in)
    return


# =============================================================
# LISTAR PERSONAL SIN USUARIO
# =============================================================
@router.get("/personal/sin-usuario", response_model=List[PersonalRead])
def get_personal_sin_usuario(
    db: Session = Depends(get_db),
    _: dict = Depends(require_permissions(["USUARIOS_CREAR"])),
):
    """
    Devuelve el personal que aún no tiene un usuario asignado.
    """
    return personal_sin_usuario(db)
