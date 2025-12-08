from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
from pydantic import BaseModel

from app.db.session import get_db
from app.models.usuario import Usuario
from app.models.permiso import Permiso
from app.models.role_permiso import RolPermiso
from app.core.security import verify_password, create_access_token
from app.schemas.auth import LoginResponse, UserInToken, Token

router = APIRouter(prefix="/auth", tags=["Auth"])

class LoginRequest(BaseModel):
    email: str
    password: str

@router.post("/login", response_model=LoginResponse)
def login(request: LoginRequest, db: Session = Depends(get_db)):

    usuario = db.query(Usuario).filter(Usuario.email == request.email).first()
    if not usuario:
        raise HTTPException(status_code=401, detail="Correo o contraseña incorrectos.")
    if not verify_password(request.password, usuario.hashed_password):
        raise HTTPException(status_code=401, detail="Correo o contraseña incorrectos.")
    if not usuario.activo:
        raise HTTPException(status_code=403, detail="Tu cuenta está inactiva.")

    permisos = (
        db.query(Permiso.codigo)
        .join(RolPermiso, RolPermiso.permiso_id == Permiso.id)
        .filter(RolPermiso.rol_id == usuario.rol_id)
        .all()
    )
    permisos_list = [p[0] for p in permisos]

    token = create_access_token({
        "sub": str(usuario.id),
        "email": usuario.email,
        "rol_id": usuario.rol_id,
    })

    usuario.ultimo_login = datetime.utcnow()
    db.commit()

    return LoginResponse(
        token=Token(access_token=token),
        user=UserInToken(
            id=usuario.id,
            nombres=usuario.nombres,
            apellido_paterno=usuario.apellido_paterno,
            apellido_materno=usuario.apellido_materno,
            email=usuario.email,
            rol_id=usuario.rol_id,
            rol_nombre=usuario.rol.nombre,
            permisos=permisos_list
        )
    )
