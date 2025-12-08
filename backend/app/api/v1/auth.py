# app/api/v1/auth.py
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import datetime
from typing import List
from app.db.session import get_db
from app.core.security import verify_password, create_access_token
from app.schemas.auth import LoginRequest, LoginResponse, Token, UserInToken
from app.models.usuario import Usuario
from app.models.permiso import Permiso
from app.models.rol import Rol
from app.api.deps import get_current_active_user


router = APIRouter()


# ==================================================
# LOGIN - AUTENTICACIÓN
# ==================================================
@router.post("/login", response_model=LoginResponse)
def login(
    credentials: LoginRequest,
    db: Session = Depends(get_db)
):
    """
    Endpoint de autenticación (login)
    
    - **email**: Email del usuario
    - **password**: Contraseña del usuario
    
    Returns:
        LoginResponse con token JWT y datos del usuario
    """
    # Buscar usuario por email
    usuario = db.query(Usuario).filter(Usuario.email == credentials.email).first()
    
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales incorrectas"
        )
    
    # Verificar contraseña
    if not verify_password(credentials.password, usuario.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales incorrectas"
        )
    
    # Verificar que el usuario esté activo
    if not usuario.activo:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Usuario inactivo. Contacte al administrador."
        )
    
    # Obtener rol y permisos
    rol = db.query(Rol).filter(Rol.id == usuario.rol_id).first()
    
    # Obtener permisos del rol
    permisos = (
        db.query(Permiso.codigo)
        .join(Rol.permisos)
        .filter(Rol.id == usuario.rol_id)
        .all()
    )
    permisos_lista = [p[0] for p in permisos]
    
    # Actualizar último login
    usuario.ultimo_login = datetime.utcnow()
    db.commit()
    
    # Crear token JWT
    token_data = {
        "user_id": usuario.id,
        "email": usuario.email,
        "rol_id": usuario.rol_id
    }
    access_token = create_access_token(data=token_data)
    
    # Preparar respuesta
    user_data = UserInToken(
        id=usuario.id,
        nombres=usuario.nombres,
        apellido_paterno=usuario.apellido_paterno,
        apellido_materno=usuario.apellido_materno,
        email=usuario.email,
        rol_id=usuario.rol_id,
        rol_nombre=rol.nombre if rol else None,
        permisos=permisos_lista
    )
    
    return LoginResponse(
        token=Token(access_token=access_token, token_type="bearer"),
        user=user_data
    )


# ==================================================
# LOGIN ALTERNATIVO - OAuth2PasswordRequestForm
# ==================================================
@router.post("/token", response_model=Token)
def login_oauth2(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    """
    Endpoint alternativo de login compatible con OAuth2
    Usa formulario estándar (username y password)
    """
    # Buscar usuario por email (username)
    usuario = db.query(Usuario).filter(Usuario.email == form_data.username).first()
    
    if not usuario or not verify_password(form_data.password, usuario.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales incorrectas",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    if not usuario.activo:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Usuario inactivo"
        )
    
    # Actualizar último login
    usuario.ultimo_login = datetime.utcnow()
    db.commit()
    
    # Crear token
    token_data = {
        "user_id": usuario.id,
        "email": usuario.email,
        "rol_id": usuario.rol_id
    }
    access_token = create_access_token(data=token_data)
    
    return Token(access_token=access_token, token_type="bearer")


# ==================================================
# ME - OBTENER USUARIO ACTUAL
# ==================================================
@router.get("/me", response_model=UserInToken)
def get_me(
    current_user: Usuario = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Obtiene la información del usuario autenticado actual
    """
    # Obtener rol
    rol = db.query(Rol).filter(Rol.id == current_user.rol_id).first()
    
    # Obtener permisos
    permisos = (
        db.query(Permiso.codigo)
        .join(Rol.permisos)
        .filter(Rol.id == current_user.rol_id)
        .all()
    )
    permisos_lista = [p[0] for p in permisos]
    
    return UserInToken(
        id=current_user.id,
        nombres=current_user.nombres,
        apellido_paterno=current_user.apellido_paterno,
        apellido_materno=current_user.apellido_materno,
        email=current_user.email,
        rol_id=current_user.rol_id,
        rol_nombre=rol.nombre if rol else None,
        permisos=permisos_lista
    )


# ==================================================
# LOGOUT (OPCIONAL - Cliente debe eliminar el token)
# ==================================================
@router.post("/logout")
def logout(
    current_user: Usuario = Depends(get_current_active_user)
):
    """
    Endpoint de logout (opcional)
    
    Nota: En JWT sin estado, el cliente debe eliminar el token.
    Este endpoint existe solo para confirmar el cierre de sesión.
    """
    return {
        "message": "Sesión cerrada exitosamente",
        "user": current_user.email
    }
