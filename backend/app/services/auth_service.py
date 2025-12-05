# app/services/auth_service.py
from datetime import datetime
from typing import Tuple, List

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.usuario import Usuario
from app.models.rol import Rol
from app.core.security import verify_password, create_access_token, create_refresh_token


def get_user_permissions(db: Session, rol: Rol) -> List[str]:
    """
    Devuelve la lista de códigos de permisos asociados a ese rol.
    """
    if not rol or not rol.permisos:
        return []
    return [p.codigo for p in rol.permisos]


def autenticar_usuario(db: Session, email: str, password: str) -> Tuple[Usuario, str, str]:
    user = db.query(Usuario).filter(Usuario.email == email).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Correo o contraseña incorrectos."
        )

    if not verify_password(password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Correo o contraseña incorrectos."
        )

    if not user.activo:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Tu cuenta está inactiva."
        )

    # actualizar último login
    user.ultimo_login = datetime.utcnow()
    db.add(user)
    db.commit()
    db.refresh(user)

    access_token = create_access_token({"sub": str(user.id), "rol_id": user.rol_id})
    refresh_token = create_refresh_token({"sub": str(user.id)})

    return user, access_token, refresh_token
