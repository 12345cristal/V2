# app/services/roles_service.py

from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.models.roles import Rol
from app.models.permisos import Permiso
from app.models.roles_permisos import RolPermiso


class RolesService:

    @staticmethod
    def listar(db: Session):
        return db.query(Rol).all()

    @staticmethod
    def permisos_de_rol(rol_id: int, db: Session):
        rol = db.query(Rol).filter(Rol.id == rol_id).first()
        if not rol:
            raise HTTPException(404, "Rol no encontrado")

        permisos = (
            db.query(Permiso)
            .join(RolPermiso)
            .filter(RolPermiso.rol_id == rol_id)
            .all()
        )
        return permisos
