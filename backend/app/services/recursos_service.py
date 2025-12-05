# app/services/recursos_service.py

from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.models.recursos_terapeuta import Recurso
from app.models.recursos_tareas import RecursoTarea


class RecursosService:

    @staticmethod
    def listar(filtros, db: Session):
        q = db.query(Recurso)
        if filtros.texto:
            q = q.filter(Recurso.titulo.like(f"%{filtros.texto}%"))
        return q.all()

    @staticmethod
    def crear(dto, db: Session):
        r = Recurso(**dto)
        db.add(r)
        db.commit()
        db.refresh(r)
        return r

    @staticmethod
    def tareas_de_recurso(id: int, db: Session):
        return db.query(RecursoTarea).filter(RecursoTarea.recurso_id == id).all()
