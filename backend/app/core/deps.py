# app/core/deps.py
from typing import Generator, List, Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session, joinedload

from app.core.security import decode_token
from app.db.session import SessionLocal
from app.models.usuario import Usuario
from app.models.rol import Rol
from app.models.rol_permiso import RolPermiso
from app.models.permiso import Permiso


reusable_oauth2 = HTTPBearer(auto_error=False)


# ==========================
# DB SESSION
# ==========================

def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ==========================
# USUARIO ACTUAL
# ==========================

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(reusable_oauth2),
    db: Session = Depends(get_db),
) -> Usuario:
    if credentials is None or not credentials.scheme.lower() == "bearer":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="No se proporcionó token de autenticación.",
        )

    token = credentials.credentials
    try:
        payload = decode_token(token, token_type="access")
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido o expirado.",
        )

    user_id: Optional[str] = payload.get("sub")
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido.",
        )

    user = (
        db.query(Usuario)
        .options(joinedload(Usuario.rol))
        .filter(Usuario.id == int(user_id))
        .first()
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario no encontrado.",
        )

    return user


def get_current_active_user(
    current_user: Usuario = Depends(get_current_user),
) -> Usuario:
    if not current_user.activo:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Usuario inactivo o bloqueado.",
        )
    return current_user


# ==========================
# ROLES / PERMISOS
# ==========================

def _get_permisos_de_rol(db: Session, rol_id: int) -> List[str]:
    q = (
        db.query(Permiso.codigo)
        .join(RolPermiso, RolPermiso.permiso_id == Permiso.id)
        .join(Rol, Rol.id == RolPermiso.rol_id)
        .filter(Rol.id == rol_id)
    )
    return [row[0] for row in q.all()]


def require_roles(*role_ids: int):
    """
    Uso:
    @router.get("/algo", dependencies=[Depends(require_roles(1,2))])
    """

    def dependency(
        current_user: Usuario = Depends(get_current_active_user),
    ) -> Usuario:
        if current_user.rol_id not in role_ids:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="No tienes el rol requerido.",
            )
        return current_user

    return dependency


def require_permissions(*required_permissions: str):
    """
    Uso:
    @router.get("/algo", dependencies=[Depends(require_permissions("ninos.ver"))])
    """

    def dependency(
        current_user: Usuario = Depends(get_current_active_user),
        db: Session = Depends(get_db),
    ) -> Usuario:
        permisos = _get_permisos_de_rol(db, current_user.rol_id)
        if not any(p in permisos for p in required_permissions):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="No tienes permisos suficientes.",
            )
        return current_user

    return dependency
