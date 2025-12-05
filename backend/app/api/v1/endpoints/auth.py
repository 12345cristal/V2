from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.services.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["auth"])


class LoginRequest(BaseModel):
    email: str
    password: str


@router.post("/login")
def login(payload: LoginRequest, db: Session = Depends(get_db)):
    """
    POST /auth/login
    Body: { "email": string, "password": string }

    Respuesta:
    {
      "token": {
        "access_token": "...",
        "token_type": "bearer"
      },
      "refresh_token": "...",
      "user": {
        "id": 1,
        "nombres": "...",
        "apellido_paterno": "...",
        "apellido_materno": "...",
        "email": "...",
        "rol_id": 3,
        "rol_nombre": "TERAPEUTA",
        "permisos": ["ninos.ver", ...]
      }
    }
    """
    return AuthService.login(payload.email, payload.password, db)


@router.post("/refresh")
def refresh_token(current_user_id: int = Depends(...)):
    # aquí normalmente decodificas refresh_token; simplificado
    return {
        "token": AuthService.refresh(current_user_id)
    }
