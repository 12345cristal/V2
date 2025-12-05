# app/api/v1/endpoints/auth.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.deps import get_db, get_current_active_user
from app.core.security import decode_token
from app.schemas.auth import LoginRequest, LoginResponse, Token, UserInToken
from app.services.auth_service import (
    autenticar_usuario,
    generar_tokens_para_usuario,
)
from app.utils.auditoria import registrar_auditoria
from app.models.usuario import Usuario

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login", response_model=LoginResponse)
def login(
    body: LoginRequest,
    db: Session = Depends(get_db),
):
    usuario, permisos = autenticar_usuario(db, body.email, body.password)
    access_token, refresh_token = generar_tokens_para_usuario(usuario, permisos)

    # Commit de último_login
    db.commit()

    # Auditoría
    registrar_auditoria(
        db=db,
        usuario_id=usuario.id,
        accion="LOGIN",
        tabla_afectada="usuarios",
        registro_id=usuario.id,
    )
    db.commit()

    user_token = UserInToken(
        id=usuario.id,
        nombres=usuario.nombres,
        apellido_paterno=usuario.apellido_paterno,
        apellido_materno=usuario.apellido_materno,
        email=usuario.email,
        rol_id=usuario.rol_id,
        rol_nombre=usuario.rol.nombre if usuario.rol else None,
        permisos=permisos,
    )

    return LoginResponse(
        token=Token(access_token=access_token),
        refresh_token=refresh_token,
        user=user_token,
    )


@router.post("/refresh", response_model=LoginResponse)
def refresh_token(
    token: Token,
    db: Session = Depends(get_db),
):
    """
    Recibe:
    {
      "access_token": "<no importa>",
      "token_type": "bearer",
      "refresh_token": "<REFRESH>"
    }
    pero para simplificar, solo usamos token.access_token como refresh.
    """
    try:
        payload = decode_token(token.access_token, token_type="refresh")
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token inválido o expirado.",
        )

    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token inválido.",
        )

    usuario: Usuario | None = db.query(Usuario).get(int(user_id))
    if not usuario or not usuario.activo:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Usuario inactivo o no encontrado.",
        )

    from app.core.deps import _get_permisos_de_rol  # evitar ciclo
    permisos = _get_permisos_de_rol(db, usuario.rol_id)
    access_token, new_refresh_token = generar_tokens_para_usuario(usuario, permisos)

    db.commit()

    user_token = UserInToken(
        id=usuario.id,
        nombres=usuario.nombres,
        apellido_paterno=usuario.apellido_paterno,
        apellido_materno=usuario.apellido_materno,
        email=usuario.email,
        rol_id=usuario.rol_id,
        rol_nombre=usuario.rol.nombre if usuario.rol else None,
        permisos=permisos,
    )

    return LoginResponse(
        token=Token(access_token=access_token),
        refresh_token=new_refresh_token,
        user=user_token,
    )
