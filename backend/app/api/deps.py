# app/api/deps.py
from typing import List, Callable

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.security import decode_token
from app.db.session import get_db
from app.models.usuario import Usuario
from app.models.rol import Rol

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.API_V1_PREFIX}/auth/login")


def get_current_user(
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme)
) -> Usuario:
    try:
        payload = decode_token(token)
        user_id: str = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token inválido.")
    except Exception:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token inválido.")

    user = db.query(Usuario).filter(Usuario.id == int(user_id)).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Usuario no encontrado.")

    return user


def get_current_active_user(
    current_user: Usuario = Depends(get_current_user)
) -> Usuario:
    if not current_user.activo:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Usuario inactivo."
        )
    return current_user


# ---------- ROLES ----------

def require_roles(*allowed_roles: int) -> Callable:
    def role_checker(
        current_user: Usuario = Depends(get_current_active_user)
    ) -> Usuario:
        if allowed_roles and current_user.rol_id not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="No tienes permisos para acceder a este recurso."
            )
        return current_user
    return role_checker


# ---------- PERMISOS ----------

def require_permissions(*required_perms: str) -> Callable:
    from app.models.rol import Rol  # evitar import circular

    def perm_checker(
        db: Session = Depends(get_db),
        current_user: Usuario = Depends(get_current_active_user)
    ) -> Usuario:
        rol: Rol = db.query(Rol).filter(Rol.id == current_user.rol_id).first()
        if not rol or not rol.permisos:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="No tienes permisos asignados."
            )

        permisos_user = {p.codigo for p in rol.permisos}
        if required_perms and not any(rp in permisos_user for rp in required_perms):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="No tienes los permisos necesarios."
            )

        return current_user

    return perm_checker
