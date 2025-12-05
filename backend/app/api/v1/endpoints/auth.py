# app/api/v1/endpoints/auth.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.schemas.auth import LoginRequest, LoginResponse, UserResponse, TokenData
from app.services.auth_service import autenticar_usuario, get_user_permissions
from app.api.deps import get_current_active_user
from app.db.session import get_db
from app.models.usuario import Usuario
from app.core.security import decode_token, create_access_token

router = APIRouter()


@router.post("/login", response_model=LoginResponse)
def login(data: LoginRequest, db: Session = Depends(get_db)):

    user, access_token, refresh_token = autenticar_usuario(db, data.email, data.password)

    permisos = get_user_permissions(db, user.rol)

    return LoginResponse(
        token=TokenData(
            access_token=access_token,
            token_type="bearer",
            refresh_token=refresh_token
        ),
        user=UserResponse(
            id=user.id,
            nombres=user.nombres,
            apellido_paterno=user.apellido_paterno,
            apellido_materno=user.apellido_materno,
            email=user.email,
            rol_id=user.rol_id,
            rol_nombre=user.rol.nombre if user.rol else None,
            permisos=permisos
        )
    )


@router.get("/me", response_model=UserResponse)
def get_me(current_user: Usuario = Depends(get_current_active_user), db: Session = Depends(get_db)):
    permisos = get_user_permissions(db, current_user.rol)
    return UserResponse(
        id=current_user.id,
        nombres=current_user.nombres,
        apellido_paterno=current_user.apellido_paterno,
        apellido_materno=current_user.apellido_materno,
        email=current_user.email,
        rol_id=current_user.rol_id,
        rol_nombre=current_user.rol.nombre if current_user.rol else None,
        permisos=permisos
    )


@router.post("/refresh", response_model=TokenData)
def refresh_token(refresh_token: str):
    """
    Recibe un refresh_token (por body).
    Puedes luego moverlo a cookie httpOnly si quieres más seguridad.
    """
    try:
        payload = decode_token(refresh_token)
        if payload.get("type") != "refresh":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Token de refresh inválido."
            )

        user_id = payload.get("sub")
        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Token inválido."
            )

        new_access = create_access_token({"sub": user_id})
        return TokenData(access_token=new_access, token_type="bearer", refresh_token=refresh_token)

    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token inválido o expirado."
        )
