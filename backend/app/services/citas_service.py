# app/services/citas_service.py

from sqlalchemy.orm import Session
from fastapi import HTTPException
from datetime import datetime, timedelta

from app.models.citas import Cita


class CitasService:

    @staticmethod
    def listar(fecha, estado, nino, db: Session):
        q = db.query(Cita)
        if fecha:
            q = q.filter(Cita.fecha == fecha)
        if estado:
            q = q.filter(Cita.estado_id == estado)
        if nino:
            q = q.filter(Cita.nino_id == nino)
        return q.all()

    @staticmethod
    def crear(dto, db: Session):
        cita = Cita(**dto)
        db.add(cita)
        db.commit()
        db.refresh(cita)
        return cita

    @staticmethod
    def actualizar(id: int, dto, db: Session):
        c = db.query(Cita).filter(Cita.id == id).first()
        if not c:
            raise HTTPException(404, "Cita no encontrada")
        for k, v in dto.items():
            setattr(c, k, v)
        db.commit()
        return c

    @staticmethod
    def cancelar(id: int, motivo: str, db: Session):
        c = db.query(Cita).filter(Cita.id == id).first()
        if not c:
            raise HTTPException(404, "Cita no encontrada")
        c.estado_id = 3  # CANCELADA
        c.motivo = motivo
        db.commit()
        return c
