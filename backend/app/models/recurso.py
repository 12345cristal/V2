# app/models/recurso.py
from sqlalchemy import Column, Integer, String, Text, ForeignKey, SmallInteger, DateTime, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.base_class import Base


class Recurso(Base):
    """
    Modelo para la tabla 'recursos'
    Recursos educativos y terapéuticos creados por el personal
    """
    __tablename__ = "recursos"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    personal_id = Column(Integer, ForeignKey("personal.id", ondelete="SET NULL"))
    titulo = Column(String(200), nullable=False)
    descripcion = Column(Text)
    tipo_id = Column(SmallInteger, ForeignKey("tipo_recurso.id"))
    categoria_id = Column(SmallInteger, ForeignKey("categoria_recurso.id"))
    nivel_id = Column(SmallInteger, ForeignKey("nivel_recurso.id"))
    
    # Tags para búsqueda y filtrado
    etiquetas = Column(JSON)  # Lista de palabras clave
    
    # URL o path del archivo
    archivo_url = Column(String(500))
    
    # Metadata
    es_destacado = Column(SmallInteger, default=0)
    fecha_publicacion = Column(DateTime, default=datetime.utcnow)
    fecha_modificacion = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    activo = Column(SmallInteger, default=1)

    # Relaciones
    personal = relationship("Personal", foreign_keys=[personal_id])
    tipo = relationship("TipoRecurso")
    categoria = relationship("CategoriaRecurso")
    nivel = relationship("NivelRecurso")
    tareas_asignadas = relationship("TareaRecurso", back_populates="recurso", cascade="all, delete-orphan")


class TipoRecurso(Base):
    """
    Catálogo de tipos de recurso (PDF, Video, Imagen, Enlace, etc.)
    """
    __tablename__ = "tipo_recurso"

    id = Column(SmallInteger, primary_key=True, autoincrement=True)
    codigo = Column(String(30), nullable=False, unique=True)
    nombre = Column(String(80), nullable=False)
    descripcion = Column(String(200))

    # Relaciones
    recursos = relationship("Recurso", back_populates="tipo")


class CategoriaRecurso(Base):
    """
    Catálogo de categorías de recurso (Motricidad, Lenguaje, Conductual, etc.)
    """
    __tablename__ = "categoria_recurso"

    id = Column(SmallInteger, primary_key=True, autoincrement=True)
    codigo = Column(String(30), nullable=False, unique=True)
    nombre = Column(String(80), nullable=False)
    descripcion = Column(String(200))

    # Relaciones
    recursos = relationship("Recurso", back_populates="categoria")


class NivelRecurso(Base):
    """
    Catálogo de niveles de dificultad (Básico, Intermedio, Avanzado)
    """
    __tablename__ = "nivel_recurso"

    id = Column(SmallInteger, primary_key=True, autoincrement=True)
    codigo = Column(String(30), nullable=False, unique=True)
    nombre = Column(String(80), nullable=False)
    orden = Column(SmallInteger, default=0)

    # Relaciones
    recursos = relationship("Recurso", back_populates="nivel")
