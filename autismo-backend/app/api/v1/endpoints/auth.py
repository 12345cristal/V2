# app/api/v1/endpoints/auth.py
"""Endpoints de autenticación"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime

from app.db.session import get_db
from app.models.usuario import Usuario
from app.models.permiso import Permiso
from app.models.role_permiso import RolePermiso
from app.core.security import (
    verify_password,
    create_access_token,
    hash_password,
    get_current_active_user
)
from app.schemas.auth import (
    LoginRequest,
    LoginResponse,
    UserInToken,
    Token,
    ChangePasswordRequest
)

router = APIRouter(prefix="/auth", tags=["Autenticación"])


@router.post("/login", response_model=LoginResponse)
def login(request: LoginRequest, db: Session = Depends(get_db)):
    """
    Login de usuario con email y contraseña.
    Retorna JWT token y datos del usuario con sus permisos.
    """
    # Buscar usuario por email
    usuario = db.query(Usuario).filter(Usuario.email == request.email).first()
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Correo o contraseña incorrectos"
        )
    
    # Verificar contraseña
    if not verify_password(request.password, usuario.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Correo o contraseña incorrectos"
        )
    
    # Verificar que esté activo
    if not usuario.activo:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Tu cuenta está inactiva"
        )
    
    # Obtener permisos del rol
    permisos = (
        db.query(Permiso.codigo)
        .join(RolePermiso, RolePermiso.permiso_id == Permiso.id)
        .filter(RolePermiso.rol_id == usuario.rol_id)
        .all()
    )
    permisos_list = [p[0] for p in permisos]
    
    # Crear token JWT
    token = create_access_token({
        "sub": str(usuario.id),
        "email": usuario.email,
        "rol_id": usuario.rol_id,
    })
    
    # Actualizar último login
    usuario.ultimo_login = datetime.utcnow()
    db.commit()
    
    # Respuesta
    return LoginResponse(
        token=Token(access_token=token),
        user=UserInToken(
            id=usuario.id,
            nombres=usuario.nombres,
            apellido_paterno=usuario.apellido_paterno,
            apellido_materno=usuario.apellido_materno,
            email=usuario.email,
            rol_id=usuario.rol_id,
            rol_nombre=usuario.rol.nombre if usuario.rol else None,
            permisos=permisos_list
        )
    )


@router.post("/change-password")
def change_password(
    request: ChangePasswordRequest,
    current_user: Usuario = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Cambiar contraseña del usuario actual"""
    # Verificar contraseña actual
    if not verify_password(request.current_password, current_user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Contraseña actual incorrecta"
        )
    
    # Actualizar contraseña
    current_user.hashed_password = hash_password(request.new_password)
    db.commit()
    
    return {"message": "Contraseña actualizada exitosamente"}


@router.get("/me", response_model=UserInToken)
def get_current_user_info(
    current_user: Usuario = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Obtener información del usuario actual"""
    # Obtener permisos
    permisos = (
        db.query(Permiso.codigo)
        .join(RolePermiso, RolePermiso.permiso_id == Permiso.id)
        .filter(RolePermiso.rol_id == current_user.rol_id)
        .all()
    )
    permisos_list = [p[0] for p in permisos]
    
    return UserInToken(
        id=current_user.id,
        nombres=current_user.nombres,
        apellido_paterno=current_user.apellido_paterno,
        apellido_materno=current_user.apellido_materno,
        email=current_user.email,
        rol_id=current_user.rol_id,
        rol_nombre=current_user.rol.nombre if current_user.rol else None,
        permisos=permisos_list
    )
