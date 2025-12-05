# app/api/deps.py
from typing import Generator, List
from fastapi import Depends, HTTPException, status
from jose import jwt, JWTError
from sqlalchemy.orm import Session

from app.db.session import SessionLocal
from app.core.config import settings
from app.models.usuario import Usuario
from app.models.permiso import Permiso, RolPermiso
from app.models.rol import Rol


def get_db() -> Generator:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_current_user(
    db: Session = Depends(get_db),
    token: str = Depends(...)
):
    # Para usar OAuth2PasswordBearer, define en auth.py
    from fastapi.security import OAuth2PasswordBearer
    oauth2_scheme = OAuth2PasswordBearer(
        tokenUrl=f"{settings.API_V1_PREFIX}/auth/login"
    )
    _token = yield from oauth2_scheme()

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No se pudo validar las credenciales.",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            _token,
            settings.JWT_SECRET_KEY,
            algorithms=[settings.JWT_ALGORITHM],
        )
        user_id: str | None = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = db.query(Usuario).filter(Usuario.id_usuario == int(user_id)).first()
    if not user:
        raise credentials_exception
    return user


def get_current_active_user(current_user: Usuario = Depends(get_current_user)):
    if current_user.estado != "ACTIVO":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Usuario inactivo o bloqueado",
        )
    return current_user


def require_permissions(required: List[str]):
    def dependency(
        current_user: Usuario = Depends(get_current_active_user),
        db: Session = Depends(get_db)
    ):
        # obten códigos de permisos del rol
        rol = current_user.rol_sistema
        rol_obj = db.query(Rol).filter(Rol.nombre_rol == rol).first()
        if not rol_obj:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Rol no configurado"
            )

        rol_permisos = (
            db.query(Permiso.codigo)
            .join(RolPermiso, RolPermiso.id_permiso == Permiso.id_permiso)
            .filter(RolPermiso.id_rol == rol_obj.id_rol)
            .all()
        )
        codes = {p[0] for p in rol_permisos}
        if not any(r in codes for r in required):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="No tienes permisos suficientes"
            )
        return current_user

    return dependency
