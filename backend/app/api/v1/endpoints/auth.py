# app/api/v1/endpoints/auth.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.schemas.auth import LoginResponse
from app.services.auth_service import autenticar_usuario

router = APIRouter(prefix="/auth", tags=["auth"])


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


@router.post("/login", response_model=LoginResponse)
def login(request: LoginRequest, db: Session = Depends(get_db)):
    """
    Endpoint de login que regresa exactamente lo que espera tu frontend:
    {
      token: { access_token, token_type },
      user: { id, nombres, ..., rol_id, rol_nombre, permisos }
    }
    """
    return autenticar_usuario(db, request.email, request.password)
