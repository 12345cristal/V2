# app/services/auth_service.py
from datetime import datetime
from typing import List, Tuple

from fastapi import HTTPException, status
from sqlalchemy.orm import Session, joinedload

from app.core.security import verify_password, create_access_token, create_refresh_token
from app.models.usuario import Usuario
from app.models.rol import Rol
from app.models.rol_permiso import RolPermiso
from app.models.permiso import Permiso


def _get_permisos_de_rol(db: Session, rol_id: int) -> List[str]:
    q = (
        db.query(Permiso.codigo)
        .join(RolPermiso, RolPermiso.permiso_id == Permiso.id)
        .join(Rol, Rol.id == RolPermiso.rol_id)
        .filter(Rol.id == rol_id)
    )
    return [row[0] for row in q.all()]


def autenticar_usuario(
    db: Session,
    email: str,
    password: str,
) -> Tuple[Usuario, List[str]]:
    usuario = (
        db.query(Usuario)
        .options(joinedload(Usuario.rol))
        .filter(Usuario.email == email)
        .first()
    )

    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Correo o contraseña incorrectos.",
        )

    if not usuario.activo:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Tu cuenta está inactiva.",
        )

    if not verify_password(password, usuario.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Correo o contraseña incorrectos.",
        )

    permisos = _get_permisos_de_rol(db, usuario.rol_id)

    usuario.ultimo_login = datetime.utcnow()
    db.add(usuario)

    return usuario, permisos


def generar_tokens_para_usuario(
    usuario: Usuario,
    permisos: List[str],
) -> Tuple[str, str]:
    claims = {
        "rol_id": usuario.rol_id,
        "permisos": permisos,
    }
    access = create_access_token(subject=usuario.id, extra_claims=claims)
    refresh = create_refresh_token(subject=usuario.id, extra_claims=claims)
    return access, refresh
