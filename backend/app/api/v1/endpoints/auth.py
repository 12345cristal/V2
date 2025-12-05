# app/api/v1/endpoints/auth.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.schemas.auth import LoginRequest, LoginResponse, UserResponse, TokenResponse
from app.services.auth_service import autenticar_usuario
from app.db.session import get_db

router = APIRouter()

@router.post("/login", response_model=LoginResponse)
def login(data: LoginRequest, db: Session = Depends(get_db)):
    user, token = autenticar_usuario(db, data.correo, data.contrasena)

    return LoginResponse(
        token=TokenResponse(access_token=token),
        user=UserResponse(
            id=user.id,
            nombres=user.nombres,
            email=user.email,
            rol_id=user.rol_id
        )
    )
