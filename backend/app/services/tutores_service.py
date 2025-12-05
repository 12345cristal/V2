# app/services/tutores_service.py

from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.models.tutores import Tutor
from app.models.tutores_direccion import TutorDireccion


class TutoresService:

    @staticmethod
    def obtener(id: int, db: Session):
        t = db.query(Tutor).filter(Tutor.id == id).first()
        if not t:
            raise HTTPException(404, "Tutor no encontrado")
        return t
