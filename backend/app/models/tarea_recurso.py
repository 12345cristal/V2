# app/models/tarea_recurso.py

from sqlalchemy import Column, Integer, ForeignKey, Boolean, DateTime, func
from sqlalchemy.orm import relationship
from app.db.base_class import Base


class TareaRecurso(Base):
    __tablename__ = "tareas_recurso"

    id = Column(Integer, primary_key=True, index=True)
    recurso_id = Column(Integer, ForeignKey("recursos_terapeuta.id"), nullable=False)
    nino_id = Column(Integer, index=True, nullable=False)
    completado = Column(Boolean, default=False)
    fecha_asignacion = Column(DateTime, server_default=func.now())
    fecha_completado = Column(DateTime, nullable=True)

    recurso = relationship("RecursoTerapeuta", backref="tareas")
