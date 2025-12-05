# app/services/actividades_padre_service.py

from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.models.recursos_tareas import RecursoTarea


class ActividadesPadreService:

    @staticmethod
    def mis_actividades(tutor_id: int, db: Session):
        return (
            db.query(RecursoTarea)
            .filter(RecursoTarea.nino_id.in_(
                [n.id for n in tutor_id.ninos]
            ))
            .all()
        )

    @staticmethod
    def completar(id: int, dto, db: Session):
        t = db.query(RecursoTarea).filter(RecursoTarea.id == id).first()
        if not t:
            raise HTTPException(404, "Actividad no encontrada")
        t.completado = dto.completado
        t.comentarios_padres = dto.comentarios_padres
        db.commit()
        return t
