# app/api/v1/endpoints/auth.py
from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.security import verify_password, create_access_token
from app.db.session import get_db
from app.models.usuario import Usuario
from app.schemas.auth import LoginRequest, LoginResponse, Token, UserInToken

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login", response_model=LoginResponse)
def login(
    data: LoginRequest,
    db: Session = Depends(get_db),
):
    usuario = db.query(Usuario).filter(Usuario.email == data.email).first()
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales incorrectas",
        )
    if not verify_password(data.password, usuario.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales incorrectas",
        )
    if not usuario.activo:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Usuario inactivo",
        )

    rol_nombre = usuario.rol.nombre if usuario.rol else ""
    permisos_codigos = [p.codigo for p in usuario.rol.permisos] if usuario.rol else []

    access_token_expires = timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )
    token_str = create_access_token(
        subject=usuario.id,
        expires_delta=access_token_expires,
        extra_claims={
            "rol": rol_nombre,
            "permisos": permisos_codigos,
        },
    )

    token = Token(access_token=token_str)
    user_info = UserInToken(
        id=usuario.id,
        nombres=usuario.nombres,
        apellido_paterno=usuario.apellido_paterno,
        apellido_materno=usuario.apellido_materno,
        email=usuario.email,
        rol=rol_nombre,
        permisos=permisos_codigos,
    )
    return LoginResponse(token=token, user=user_info)


@router.get("/me", response_model=UserInToken)
def read_me(
    current_user: Usuario = Depends(
        lambda: None  # se remplaza en main con un Depends adecuado
    ),
):
    # Esto lo ajustaremos en main para usar get_current_active_user
    raise HTTPException(status_code=500, detail="No implementado")
