# app/services/ninos_service.py

from sqlalchemy.orm import Session
from fastapi import HTTPException, UploadFile
import uuid

from app.models.ninos import Nino
from app.models.ninos_diagnostico import NinoDiagnostico
from app.models.ninos_info_emocional import NinoInfoEmocional


class NinosService:

    # -----------------------------------------------------------
    # LISTAR
    # -----------------------------------------------------------
    @staticmethod
    def listar(search: str | None, estado: str | None, db: Session):
        q = db.query(Nino)
        if search:
            q = q.filter(Nino.nombre.like(f"%{search}%"))
        if estado and estado != "TODOS":
            q = q.filter(Nino.estado == estado)
        return q.all()

    # -----------------------------------------------------------
    # OBTENER
    # -----------------------------------------------------------
    @staticmethod
    def obtener(id: int, db: Session):
        n = db.query(Nino).filter(Nino.id == id).first()
        if not n:
            raise HTTPException(404, "Niño no encontrado")
        return n

    # -----------------------------------------------------------
    # CREAR
    # -----------------------------------------------------------
    @staticmethod
    def crear(data, archivos, db: Session):
        n = Nino(**data)
        db.add(n)
        db.commit()
        db.refresh(n)
        return n

    # -----------------------------------------------------------
    # ACTUALIZAR
    # -----------------------------------------------------------
    @staticmethod
    def actualizar(id: int, data, archivos, db: Session):
        n = NinosService.obtener(id, db)

        for k, v in data.items():
            setattr(n, k, v)

        db.commit()
        return n
