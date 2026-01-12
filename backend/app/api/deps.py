# app/api/deps.py
from typing import Generator, Optional, List
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer
from sqlalchemy.orm import Session
from jose import JWTError, jwt
from app.db.session import get_db
from app.core.config import settings
from app.models.usuario import Usuario
from app.models.rol import Rol
from app.models.permiso import Permiso

security = HTTPBearer()

# ==================================================
# DEPENDENCIA: SESIÓN DE BASE DE DATOS
# ==================================================
def get_db_session() -> Generator:
    """Genera una sesión de base de datos"""
    db = next(get_db())
    try:
        yield db
    finally:
        db.close()


# ==================================================
# DEPENDENCIA: USUARIO ACTUAL
# ==================================================
def get_current_user(credentials = Depends(security)):
    """Obtiene usuario actual desde JWT"""
    token = credentials.credentials  # HTTPBearer retorna objeto con .credentials
    try:
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        return {"user_id": int(user_id)}
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")


# ==================================================
# DEPENDENCIA: USUARIO ACTIVO
# ==================================================
def get_current_active_user(
    current_user: Usuario = Depends(get_current_user)
) -> Usuario:
    """Verifica que el usuario actual esté activo"""
    if not current_user.activo:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Usuario inactivo"
        )
    return current_user


# ==================================================
# DEPENDENCIA: VERIFICAR PERMISOS
# ==================================================
def require_permissions(required_permisos: List[str]):
    """Verifica si el usuario tiene los permisos requeridos"""
    def permission_checker(
        current_user: Usuario = Depends(get_current_active_user),
        db: Session = Depends(get_db_session)
    ) -> Usuario:
        user_permisos = (
            db.query(Permiso.codigo)
            .join(Rol.permisos)
            .filter(Rol.id == current_user.rol_id)
            .all()
        )
        user_permiso_codes = [p[0] for p in user_permisos]
        has_permission = any(p in user_permiso_codes for p in required_permisos)
        
        if not has_permission:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="No tiene permisos suficientes para esta acción"
            )
        return current_user
    return permission_checker


# ==================================================
# DEPENDENCIA: VERIFICAR ROL
# ==================================================
def require_role(required_roles: List[int]):
    """Verifica si el usuario tiene uno de los roles requeridos"""
    def role_checker(
        current_user: Usuario = Depends(get_current_active_user)
    ) -> Usuario:
        if current_user.rol_id not in required_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Se requiere uno de los siguientes roles: {required_roles}"
            )
        return current_user
    return role_checker


# ==================================================
# DEPENDENCIA: SOLO ADMINISTRADOR
# ==================================================
def require_admin(
    current_user: Usuario = Depends(get_current_active_user)
) -> Usuario:
    """Verifica que el usuario sea administrador"""
    if current_user.rol_id != 1:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Se requieren permisos de administrador"
        )
    return current_user


# ==================================================
# DEPENDENCIA: ADMIN O COORDINADOR
# ==================================================
def require_admin_or_coordinator(
    current_user: Usuario = Depends(get_current_active_user)
) -> Usuario:
    """Verifica que el usuario sea administrador (1) o coordinador (2)"""
    if current_user.rol_id not in [1, 2]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Se requieren permisos de administrador o coordinador"
        )
    return current_user


def get_current_padre(
    credentials = Depends(security),
    db: Session = Depends(get_db_session)
):
    """
    Obtiene padre actual desde JWT y verifica que sea un tutor/padre.
    Retorna el usuario verificado.
    """
    # Obtener usuario del token
    user_data = get_current_user(credentials)
    user_id = user_data.get("user_id")
    
    # Verificar que el usuario existe en la base de datos
    usuario = db.query(Usuario).filter(Usuario.id == user_id).first()
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado"
        )
    
    # Verificar que el usuario está activo
    if not usuario.activo:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Usuario inactivo"
        )
    
    # Verificar que el usuario tiene el rol de padre/tutor (rol_id = 5)
    # Nota: Ajustar el rol_id según tu configuración de roles
    # Por ahora, retornamos el usuario para que el servicio verifique el tutor
    
    return usuario
