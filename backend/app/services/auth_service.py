# app/services/auth_service.py
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from datetime import timedelta, datetime

from app.core.security import verify_password, create_access_token
from app.core.config import settings
from app.models.usuario import Usuario
from app.models.rol import Rol
from app.models.permiso import Permiso, RolPermiso
from app.schemas.auth import UserInToken, LoginResponse


def autenticar_usuario(db: Session, email: str, password: str) -> LoginResponse:
    usuario = db.query(Usuario).filter(Usuario.email == email).first()
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales incorrectas"
        )

    if not verify_password(password, usuario.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales incorrectas"
        )

    if usuario.estado != "ACTIVO":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Tu cuenta está inactiva o bloqueada."
        )

    # permisos desde rol
    rol_obj = db.query(Rol).filter(Rol.nombre_rol == usuario.rol_sistema).first()
    rol_id = rol_obj.id_rol if rol_obj else 0
    rol_nombre = rol_obj.nombre_rol if rol_obj else usuario.rol_sistema

    permisos_codes: list[str] = []
    if rol_obj:
        q = (
            db.query(Permiso.codigo)
            .join(RolPermiso, RolPermiso.id_permiso == Permiso.id_permiso)
            .filter(RolPermiso.id_rol == rol_obj.id_rol)
        )
        permisos_codes = [row[0] for row in q.all()]

    # Actualizar última sesión
    usuario.ultima_sesion = datetime.utcnow()
    db.add(usuario)
    db.commit()
    db.refresh(usuario)

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    token = create_access_token(
        subject=usuario.id_usuario,
        expires_delta=access_token_expires
    )

    user_payload = UserInToken(
        id=usuario.id_usuario,
        nombres=usuario.personal.nombres if usuario.personal else "",
        apellido_paterno=usuario.personal.apellido_paterno if usuario.personal else "",
        apellido_materno=usuario.personal.apellido_materno if usuario.personal else None,
        email=usuario.email,
        rol_id=rol_id,
        rol_nombre=rol_nombre,
        permisos=permisos_codes,
    )

    return LoginResponse(
        token={"access_token": token, "token_type": "bearer"},
        user=user_payload
    )
