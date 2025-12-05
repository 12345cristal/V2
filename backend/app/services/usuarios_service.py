# app/services/usuarios_service.py

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.usuarios import Usuario
from app.services.auditoria_service import registrar_evento
from app.services.auth_service import AuthService


class UsuariosService:

    @staticmethod
    def listar(db: Session):
        return db.query(Usuario).all()

    @staticmethod
    def obtener(id: int, db: Session):
        usuario = db.query(Usuario).filter(Usuario.id == id).first()
        if not usuario:
            raise HTTPException(404, "Usuario no encontrado")
        return usuario

    @staticmethod
    def crear(data, db: Session):
        hashed = AuthService.hash_password(data.password)

        nuevo = Usuario(
            nombres=data.nombres,
            apellido_paterno=data.apellido_paterno,
            apellido_materno=data.apellido_materno,
            email=data.email,
            hashed_password=hashed,
            rol_id=data.rol_id,
        )

        db.add(nuevo)
        db.commit()
        db.refresh(nuevo)

        registrar_evento(
            db, nuevo.id, "CREAR_USUARIO", "usuarios", nuevo.id
        )

        return nuevo

    @staticmethod
    def actualizar(id: int, data, db: Session):
        u = UsuariosService.obtener(id, db)

        u.nombres = data.nombres
        u.apellido_paterno = data.apellido_paterno
        u.apellido_materno = data.apellido_materno
        u.email = data.email
        u.rol_id = data.rol_id

        db.commit()
        registrar_evento(db, u.id, "ACTUALIZAR_USUARIO", "usuarios", id)
        return u

    @staticmethod
    def cambiar_estado(id: int, estado: bool, db: Session):
        u = UsuariosService.obtener(id, db)
        u.activo = estado
        db.commit()
        registrar_evento(db, u.id, "CAMBIAR_ESTADO", "usuarios", id)
        return u

    @staticmethod
    def cambiar_password(id: int, nueva: str, db: Session):
        u = UsuariosService.obtener(id, db)
        u.hashed_password = AuthService.hash_password(nueva)
        db.commit()
        registrar_evento(db, u.id, "CAMBIAR_PASSWORD", "usuarios", id)
        return {"mensaje": "Contraseña actualizada"}
