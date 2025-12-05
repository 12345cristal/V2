from fastapi import Depends, HTTPException, status
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from app.core.config import settings
from app.core.security import verify_password
from app.db.session import get_db
from app.models.usuario import Usuario
from app.models.roles import Rol, Permiso

def get_current_user(db: Session = Depends(get_db), token: str = Depends(...)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Token inválido o expirado",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = db.query(Usuario).filter(Usuario.id == user_id).first()
    if not user:
        raise credentials_exception

    return user


def get_current_active_user(user: Usuario = Depends(get_current_user)):
    if not user.activo:
        raise HTTPException(status_code=403, detail="Usuario inactivo.")
    return user


def require_permissions(*required_perms: str):
    def dependency(user: Usuario = Depends(get_current_active_user)):
        permisos_usuario = {p.codigo for p in user.rol.permisos}
        if not set(required_perms).issubset(permisos_usuario):
            raise HTTPException(status_code=403, detail="No tienes permisos para esta acción.")
        return user
    return dependency
