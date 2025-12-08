# app/models/recurso.py
"""Modelos para Recursos, Tareas y Recomendaciones IA"""

from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, SmallInteger, DECIMAL, Float, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.base_class import Base


class Recurso(Base):
    __tablename__ = "recursos"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    personal_id = Column(Integer, ForeignKey("personal.id"), nullable=False)
    titulo = Column(String(200), nullable=False)
    descripcion = Column(String, nullable=False)  # TEXT
    tipo_id = Column(SmallInteger, ForeignKey("tipo_recurso.id"))
    categoria_id = Column(SmallInteger, ForeignKey("categoria_recurso.id"))
    nivel_id = Column(SmallInteger, ForeignKey("nivel_recurso.id"))
    etiquetas = Column(String)  # TEXT
    es_destacado = Column(SmallInteger, default=0)
    es_nuevo = Column(SmallInteger, default=1)
    fecha_publicacion = Column(DateTime, default=datetime.utcnow)
    ultima_actualizacion = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    total_asignaciones = Column(Integer, default=0)
    total_completadas = Column(Integer, default=0)
    rating_promedio = Column(DECIMAL(3, 2))
    
    # Relationships
    personal = relationship("Personal", back_populates="recursos")
    tipo = relationship("TipoRecurso", back_populates="recursos")
    categoria = relationship("CategoriaRecurso", back_populates="recursos")
    nivel = relationship("NivelRecurso", back_populates="recursos")
    tareas = relationship("TareaRecurso", back_populates="recurso")
    recomendaciones = relationship("Recomendacion", back_populates="recurso")


class TareaRecurso(Base):
    __tablename__ = "tareas_recurso"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    recurso_id = Column(Integer, ForeignKey("recursos.id"), nullable=False)
    nino_id = Column(Integer, ForeignKey("ninos.id"), nullable=False)
    asignado_por = Column(Integer, ForeignKey("personal.id"))
    fecha_asignacion = Column(DateTime, default=datetime.utcnow)
    fecha_limite = Column(DateTime)
    completado = Column(SmallInteger, default=0)
    comentarios_padres = Column(String)  # TEXT
    notas_terapeuta = Column(String)  # TEXT
    
    # Relationships
    recurso = relationship("Recurso", back_populates="tareas")
    nino = relationship("Nino", back_populates="tareas")
    asignado_por_personal = relationship("Personal", back_populates="tareas_asignadas")
    valoraciones = relationship("Valoracion", back_populates="tarea")


class Valoracion(Base):
    __tablename__ = "valoraciones"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    tarea_id = Column(Integer, ForeignKey("tareas_recurso.id"), nullable=False)
    puntuacion = Column(Integer, nullable=False)  # 1-5
    comentario = Column(String)  # TEXT
    fecha = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    tarea = relationship("TareaRecurso", back_populates="valoraciones")


class Recomendacion(Base):
    __tablename__ = "recomendaciones"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    nino_id = Column(Integer, ForeignKey("ninos.id"), nullable=False)
    recurso_id = Column(Integer, ForeignKey("recursos.id"), nullable=False)
    fuente = Column(Enum('CONTENT_BASED', 'TOPSIS', 'MANUAL'), nullable=False)
    score = Column(Float, nullable=False)
    fecha = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    nino = relationship("Nino", back_populates="recomendaciones")
    recurso = relationship("Recurso", back_populates="recomendaciones")
