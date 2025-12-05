# app/services/auth_service.py

from datetime import datetime, timedelta
from fastapi import HTTPException, status, Depends
from sqlalchemy.orm import Session
from passlib.context import CryptContext

from app.models import usuarios, roles, permisos, roles_permisos
from app.core.security import create_access_token, create_refresh_token
from app.db.session import get_db
from app.services.auditoria_service import registrar_evento

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class AuthService:

    # -----------------------------------------------------------
    # Validar contraseña
    # -----------------------------------------------------------
    @staticmethod
    def verify_password(password: str, hashed: str) -> bool:
        return pwd_context.verify(password, hashed)

    @staticmethod
    def hash_password(password: str) -> str:
        return pwd_context.hash(password)

    # -----------------------------------------------------------
    # LOGIN
    # -----------------------------------------------------------
    @staticmethod
    def login(email: str, password: str, db: Session):
        usuario = db.query(usuarios.Usuario).filter(
            usuarios.Usuario.email == email
        ).first()

        if not usuario:
            raise HTTPException(status_code=401, detail="Credenciales incorrectas")

        if not AuthService.verify_password(password, usuario.hashed_password):
            raise HTTPException(status_code=401, detail="Credenciales incorrectas")

        if usuario.activo == 0:
            raise HTTPException(status_code=403, detail="Usuario inactivo")

        # Cargar permisos del rol
        rol = usuario.rol
        permisos_q = (
            db.query(permisos.Permiso.codigo)
            .join(roles_permisos.RolPermiso)
            .filter(roles_permisos.RolPermiso.rol_id == rol.id)
            .all()
        )
        permisos_lista = [p[0] for p in permisos_q]

        # Generar tokens
        access = create_access_token({"sub": str(usuario.id)})
        refresh = create_refresh_token({"sub": str(usuario.id)})

        # Actualizar último login
        usuario.ultimo_login = datetime.now()
        db.commit()

        registrar_evento(
            db=db,
            usuario_id=usuario.id,
            accion="LOGIN",
            tabla_afectada="usuarios",
            registro_id=usuario.id
        )

        return {
            "token": {
                "access_token": access,
                "token_type": "bearer"
            },
            "refresh_token": refresh,
            "user": {
                "id": usuario.id,
                "nombres": usuario.nombres,
                "apellido_paterno": usuario.apellido_paterno,
                "apellido_materno": usuario.apellido_materno,
                "email": usuario.email,
                "rol_id": usuario.rol_id,
                "rol_nombre": rol.nombre,
                "permisos": permisos_lista
            }
        }

    # -----------------------------------------------------------
    # REFRESH TOKEN
    # -----------------------------------------------------------
    @staticmethod
    def refresh(user_id: int):
        new_access = create_access_token({"sub": str(user_id)})
        return {"access_token": new_access, "token_type": "bearer"}
