# app/api/deps.py
from typing import Generator, Optional, List
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from jose import JWTError, jwt

from app.core.config import settings
from app.db.session import get_db
from app.models.usuario import Usuario
from app.models.rol import Rol
from app.models.permiso import Permiso


# ==================================================
# OAUTH2 SCHEME
# ==================================================
oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.API_V1_PREFIX}/auth/login")


# ==================================================
# DEPENDENCIA: SESIÓN DE BASE DE DATOS
# ==================================================
def get_db_session() -> Generator:
    """
    Genera una sesión de base de datos
    """
    db = next(get_db())
    try:
        yield db
    finally:
        db.close()


# ==================================================
# DEPENDENCIA: USUARIO ACTUAL
# ==================================================
def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> Usuario:
    """Obtiene el usuario actual desde el token JWT"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No se pudo validar las credenciales",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        payload = jwt.decode(
            token,
            settings.JWT_SECRET_KEY,
            algorithms=[settings.JWT_ALGORITHM]
        )
        user_id: int = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    user = db.query(Usuario).filter(Usuario.id == user_id).first()
    if user is None:
        raise credentials_exception
    
    if not user.activo:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Usuario inactivo"
        )
    
    return user


# ==================================================
# DEPENDENCIA: USUARIO ACTIVO
# ==================================================
def get_current_active_user(
    current_user: Usuario = Depends(get_current_user)
) -> Usuario:
    """
    Verifica que el usuario actual esté activo
    """
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
    """
    Crea una dependencia que verifica si el usuario tiene los permisos requeridos
    
    Args:
        required_permisos: Lista de códigos de permisos requeridos
        
    Returns:
        Función de dependencia
    """
    def permission_checker(
        current_user: Usuario = Depends(get_current_active_user),
        db: Session = Depends(get_db_session)
    ) -> Usuario:
        # Obtener permisos del usuario a través de su rol
        user_permisos = (
            db.query(Permiso.codigo)
            .join(Rol.permisos)
            .filter(Rol.id == current_user.rol_id)
            .all()
        )
        
        user_permiso_codes = [p[0] for p in user_permisos]
        
        # Verificar si tiene alguno de los permisos requeridos
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
    """
    Crea una dependencia que verifica si el usuario tiene uno de los roles requeridos
    
    Args:
        required_roles: Lista de IDs de roles permitidos (1=admin, 2=coordinador, 3=terapeuta, 4=padre)
        
    Returns:
        Función de dependencia
    """
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
    """
    Verifica que el usuario sea administrador (rol_id = 1)
    """
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
    """
    Verifica que el usuario sea administrador (1) o coordinador (2)
    """
    if current_user.rol_id not in [1, 2]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Se requieren permisos de administrador o coordinador"
        )
    return current_user
