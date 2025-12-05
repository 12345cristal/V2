from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.usuarios import Usuario
from app.models.personal import Personal
from app.models.roles import Rol
from app.services.auth_service import AuthService


class UsuariosService:

    # ============================================================
    # ROLES DEL SISTEMA
    # ============================================================
    @staticmethod
    def obtener_roles(db: Session):
        return db.query(Rol).all()

    # ============================================================
    # PERSONAL QUE AÚN NO TIENE USUARIO
    # ============================================================
    @staticmethod
    def personal_sin_usuario(db: Session):
        q = (
            db.query(Personal)
            .filter(Personal.id_personal.not_in(
                db.query(Usuario.id_personal)
            ))
            .all()
        )
        return q

    # ============================================================
    # LISTAR USUARIOS
    # ============================================================
    @staticmethod
    def listar(db: Session):
        return db.query(Usuario).all()

    # ============================================================
    # OBTENER
    # ============================================================
    @staticmethod
    def obtener(id: int, db: Session):
        return db.query(Usuario).filter(Usuario.id_usuario == id).first()

    # ============================================================
    # CREAR USUARIO
    # ============================================================
    @staticmethod
    def crear(dto, db: Session):
        if dto.password != dto.confirmarPassword:
            raise HTTPException(400, "Las contraseñas no coinciden")

        hashed = AuthService.hash_password(dto.password)

        u = Usuario(
            id_personal=dto.id_personal,
            username=dto.username,
            rol_sistema=dto.rol_sistema,
            estado=dto.estado,
            hashed_password=hashed,
            debe_cambiar_password=True
        )

        db.add(u)
        db.commit()
        db.refresh(u)
        return u

    # ============================================================
    # ACTUALIZAR USUARIO
    # ============================================================
    @staticmethod
    def actualizar(id: int, dto, db: Session):
        u = UsuariosService.obtener(id, db)
        if not u:
            raise HTTPException(404, "Usuario no encontrado")

        u.id_personal = dto.id_personal
        u.username = dto.username
        u.rol_sistema = dto.rol_sistema
        u.estado = dto.estado

        # CAMBIO DE CONTRASEÑA OPCIONAL
        if dto.cambiarPassword:
            if not dto.password or dto.password != dto.confirmarPassword:
                raise HTTPException(400, "Las contraseñas no coinciden")
            u.hashed_password = AuthService.hash_password(dto.password)
            u.debe_cambiar_password = True

        db.commit()
        return u

    # ============================================================
    # CAMBIAR ESTADO
    # ============================================================
    @staticmethod
    def cambiar_estado(id: int, db: Session):
        u = UsuariosService.obtener(id, db)
        if not u:
            raise HTTPException(404, "Usuario no encontrado")

        u.estado = "INACTIVO" if u.estado == "ACTIVO" else "ACTIVO"
        db.commit()
        return u
