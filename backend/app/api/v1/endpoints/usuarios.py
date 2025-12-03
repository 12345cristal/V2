# app/api/v1/endpoints/usuarios.py
from typing import List

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.api.deps import get_db, require_permissions
from app.core.security import hash_password
from app.models.usuario import Usuario
from app.schemas.usuario import UsuarioCreate, UsuarioUpdate, UsuarioRead

router = APIRouter(
    prefix="/usuarios",
    tags=["usuarios"],
)


@router.get(
    "/",
    response_model=List[UsuarioRead],
    dependencies=[Depends(require_permissions(["usuarios:listar"]))],
)
def list_users(
    db: Session = Depends(get_db),
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
):
    usuarios = (
        db.query(Usuario)
        .order_by(Usuario.fecha_creacion.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )
    return usuarios


@router.post(
    "/",
    response_model=UsuarioRead,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(require_permissions(["usuarios:crear"]))],
)
def create_user(
    data: UsuarioCreate,
    db: Session = Depends(get_db),
):
    existing = db.query(Usuario).filter(Usuario.email == data.email).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Ya existe un usuario con ese email",
        )

    hashed = hash_password(data.password)
    usuario = Usuario(
        nombres=data.nombres,
        apellido_paterno=data.apellido_paterno,
        apellido_materno=data.apellido_materno,
        email=data.email,
        telefono=data.telefono,
        rol_id=data.rol_id,
        hashed_password=hashed,
    )
    db.add(usuario)
    db.commit()
    db.refresh(usuario)
    return usuario


@router.get(
    "/{usuario_id}",
    response_model=UsuarioRead,
    dependencies=[Depends(require_permissions(["usuarios:listar"]))],
)
def get_user(
    usuario_id: int,
    db: Session = Depends(get_db),
):
    usuario = db.get(Usuario, usuario_id)
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado",
        )
    return usuario


@router.put(
    "/{usuario_id}",
    response_model=UsuarioRead,
    dependencies=[Depends(require_permissions(["usuarios:editar"]))],
)
def update_user(
    usuario_id: int,
    data: UsuarioUpdate,
    db: Session = Depends(get_db),
):
    usuario = db.get(Usuario, usuario_id)
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado",
        )

    payload = data.model_dump(exclude_unset=True)

    # Si viene password, actualizarla cifrada
    password = payload.pop("password", None) if "password" in payload else None
    if password:
        usuario.hashed_password = hash_password(password)

    for field, value in payload.items():
        setattr(usuario, field, value)

    db.commit()
    db.refresh(usuario)
    return usuario


@router.delete(
    "/{usuario_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(require_permissions(["usuarios:eliminar"]))],
)
def delete_user(
    usuario_id: int,
    db: Session = Depends(get_db),
):
    usuario = db.get(Usuario, usuario_id)
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado",
        )
    db.delete(usuario)
    db.commit()
    return
