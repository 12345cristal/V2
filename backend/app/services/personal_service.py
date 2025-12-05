# app/services/personal_service.py

from sqlalchemy.orm import Session
from fastapi import HTTPException, UploadFile
import uuid, os

from app.models.personal import Personal
from app.models.perfiles_personal import PerfilPersonal


class PersonalService:

    @staticmethod
    def listar(db: Session):
        return db.query(Personal).all()

    @staticmethod
    def obtener(id: int, db: Session):
        p = db.query(Personal).filter(Personal.id == id).first()
        if not p:
            raise HTTPException(404, "Personal no encontrado")
        return p

    @staticmethod
    def actualizar(id: int, data, db: Session):
        p = PersonalService.obtener(id, db)
        for k, v in data.dict().items():
            setattr(p, k, v)
        db.commit()
        return p

    @staticmethod
    def subir_cv(id: int, archivo: UploadFile, db: Session):
        filename = f"{uuid.uuid4()}_{archivo.filename}"
        path = f"uploads/cv/{filename}"
        with open(path, "wb") as f:
            f.write(archivo.file.read())

        perfil = (
            db.query(PerfilPersonal)
            .filter(PerfilPersonal.usuario_id == id)
            .first()
        )
        if perfil:
            perfil.cv_url = path
            db.commit()

        return {"cv_url": path}
