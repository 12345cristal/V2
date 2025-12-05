# app/services/terapias_service.py

from sqlalchemy.orm import Session
from fastapi import HTTPException
from datetime import datetime

from app.models.terapias import Terapia
from app.models.terapias_nino import TerapiaNino
from app.models.sesiones_terapia import SesionTerapia


class TerapiasService:

    @staticmethod
    def catalogo(db: Session):
        return db.query(Terapia).filter(Terapia.activo == 1).all()

    @staticmethod
    def asignar(dto, db: Session):
        asignacion = TerapiaNino(**dto)
        db.add(asignacion)
        db.commit()
        db.refresh(asignacion)
        return asignacion

    @staticmethod
    def registrar_sesion(id: int, data, db: Session):
        ses = SesionTerapia(
            terapia_nino_id=id,
            nivel_progreso=data["nivel_progreso"],
            nivel_colaboracion=data["nivel_colaboracion"],
            observaciones=data["observaciones"],
            asistio=True,
            fecha_sesion=datetime.now()
        )
        db.add(ses)
        db.commit()
        return ses
