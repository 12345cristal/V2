# app/api/v1/endpoints/auth.py
from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.security import verify_password, create_access_token
from app.db.session import get_db
from app.models.usuario import Usuario
from app.schemas.auth import LoginRequest, LoginResponse, Token, UserInToken
from app.api.deps import get_current_active_user

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login", response_model=LoginResponse)
def login(
    data: LoginRequest,
    db: Session = Depends(get_db),
):
    user = db.query(Usuario).filter(Usuario.email == data.email).first()
    if not user or not verify_password(data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales incorrectas",
        )

    if not user.activo:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Usuario inactivo",
        )

    rol = user.rol
    permisos = [p.codigo for p in (rol.permisos if rol else [])]

    access_token_expires = timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )
    token_str = create_access_token(
        subject=user.id,
        expires_delta=access_token_expires,
        extra_claims={
            "rol_id": rol.id if rol else None,
            "rol_nombre": rol.nombre if rol else None,
            "permisos": permisos,
        },
    )

    token = Token(access_token=token_str)
    user_payload = UserInToken(
        id=user.id,
        nombres=user.nombres,
        apellido_paterno=user.apellido_paterno,
        apellido_materno=user.apellido_materno,
        email=user.email,
        rol_id=rol.id if rol else None,
        rol_nombre=rol.nombre if rol else None,
        permisos=permisos,
    )

    return LoginResponse(token=token, user=user_payload)


@router.get("/me", response_model=UserInToken)
def read_me(
    current_user: Usuario = Depends(get_current_active_user),
):
    rol = current_user.rol
    permisos = [p.codigo for p in (rol.permisos if rol else [])]

    return UserInToken(
        id=current_user.id,
        nombres=current_user.nombres,
        apellido_paterno=current_user.apellido_paterno,
        apellido_materno=current_user.apellido_materno,
        email=current_user.email,
        rol_id=rol.id if rol else None,
        rol_nombre=rol.nombre if rol else None,
        permisos=permisos,
    )
