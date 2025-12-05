# app/models/recurso_terapeuta.py

from sqlalchemy import (
    Column, Integer, String, Text, Boolean, DateTime, Float
)
from sqlalchemy.orm import relationship
from app.db.base_class import Base
from sqlalchemy.sql import func


class RecursoTerapeuta(Base):
    __tablename__ = "recursos_terapeuta"

    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String(255), nullable=False)
    descripcion = Column(Text, nullable=False)
    tipo_id = Column(String(50), nullable=False)
    categoria_id = Column(String(50), nullable=False)
    nivel_id = Column(String(50), nullable=False)
    etiquetas = Column(String(255), nullable=True)  # ej: "lenguaje, atencion, juego"
    es_destacado = Column(Boolean, default=False)
    es_nuevo = Column(Boolean, default=False)
    fecha_publicacion = Column(DateTime, server_default=func.now())
    ultima_actualizacion = Column(
        DateTime, server_default=func.now(), onupdate=func.now()
    )
    total_asignaciones = Column(Integer, default=0)
    total_completadas = Column(Integer, default=0)
    rating_promedio = Column(Float, nullable=True)
