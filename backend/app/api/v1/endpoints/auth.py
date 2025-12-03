# app/api/v1/endpoints/auth.py
from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.security import verify_password, create_access_token
from app.db.session import get_db
from app.models.usuario import Usuario
from app.schemas.auth import LoginRequest, UserInToken, Token

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login")
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

    rol = user.rol  # lo que haya en la tabla roles
    permisos = [p.codigo for p in rol.permisos] if rol else []

    token_str = create_access_token(
        subject=user.id,
        expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
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
        rol_id=rol.id if rol else 0,
        rol_nombre=rol.nombre if rol else None,
        permisos=permisos,
    )

    return {"token": token, "user": user_payload}
