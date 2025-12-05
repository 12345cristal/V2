# app/models/actividades_recursos.py
from datetime import datetime

from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    ForeignKey,
    SmallInteger,
    Boolean,
    DateTime,
    Float,
    Numeric,
)
from sqlalchemy.orm import relationship

from app.db.base import Base


class Actividad(Base):
    __tablename__ = "actividades"

    id = Column(Integer, primary_key=True, autoincrement=True)
    titulo = Column(String(150), nullable=False)
    descripcion = Column(Text, nullable=False)
    edad_min = Column(Integer, nullable=False)
    edad_max = Column(Integer, nullable=False)
    tipo_terapia_id = Column(
        SmallInteger,
        ForeignKey("cat_tipo_terapia.id", ondelete="RESTRICT", onupdate="CASCADE"),
        nullable=False,
    )
    nivel_dificultad_id = Column(
        SmallInteger,
        ForeignKey("cat_nivel_dificultad.id", ondelete="RESTRICT", onupdate="CASCADE"),
        nullable=False,
    )
    materiales = Column(Text)
    etiquetas = Column(Text)

    tipo_terapia = relationship("CatTipoTerapia")
    nivel_dificultad = relationship("CatNivelDificultad")
    recomendaciones = relationship(
        "RecomendacionActividad", back_populates="actividad"
    )


class RecomendacionActividad(Base):
    __tablename__ = "recomendaciones_actividades"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nino_id = Column(
        Integer,
        ForeignKey("ninos.id", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False,
    )
    actividad_id = Column(
        Integer,
        ForeignKey("actividades.id", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False,
    )
    fuente = Column(String(20), nullable=False)  # 'CONTENT_BASED' / 'MANUAL'
    puntaje = Column(Float, nullable=False)
    fecha_generada = Column(DateTime, nullable=False, default=datetime.utcnow)

    nino = relationship("Nino")
    actividad = relationship("Actividad", back_populates="recomendaciones")


class RecursoTerapeuta(Base):
    __tablename__ = "recursos_terapeuta"

    id = Column(Integer, primary_key=True, autoincrement=True)
    personal_id = Column(
        Integer,
        ForeignKey("personal.id", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False,
    )
    titulo = Column(String(200))
    descripcion = Column(Text)
    tipo_id = Column(
        SmallInteger,
        ForeignKey("cat_tipo_recurso.id", ondelete="SET NULL", onupdate="CASCADE"),
    )
    categoria_id = Column(
        SmallInteger,
        ForeignKey("cat_categoria_recurso.id", ondelete="SET NULL", onupdate="CASCADE"),
    )
    nivel_id = Column(
        SmallInteger,
        ForeignKey("cat_nivel_recurso.id", ondelete="SET NULL", onupdate="CASCADE"),
    )
    etiquetas = Column(Text)
    es_destacado = Column(Boolean, default=False)
    es_nuevo = Column(Boolean, default=True)
    fecha_publicacion = Column(DateTime, default=datetime.utcnow)
    ultima_actualizacion = Column(DateTime, default=datetime.utcnow)
    total_asignaciones = Column(Integer, default=0)
    total_completadas = Column(Integer, default=0)
    rating_promedio = Column(Numeric(3, 2))

    personal = relationship("Personal")
    tipo = relationship("CatTipoRecurso")
    categoria = relationship("CatCategoriaRecurso")
    nivel = relationship("CatNivelRecurso")
    tareas = relationship("RecursoTarea", back_populates="recurso")


class RecursoTarea(Base):
    __tablename__ = "recursos_tareas"

    id = Column(Integer, primary_key=True, autoincrement=True)
    recurso_id = Column(
        Integer,
        ForeignKey("recursos_terapeuta.id", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False,
    )
    nino_id = Column(
        Integer,
        ForeignKey("ninos.id", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False,
    )
    tutor_nombre = Column(String(200))
    fecha_asignacion = Column(DateTime, default=datetime.utcnow)
    fecha_limite = Column(DateTime)
    completado = Column(Boolean, default=False)
    comentarios_padres = Column(Text)
    notas_terapeuta = Column(Text)

    recurso = relationship("RecursoTerapeuta", back_populates="tareas")
    nino = relationship("Nino")
    valoraciones = relationship("ValoracionActividad", back_populates="asignacion")


class ValoracionActividad(Base):
    __tablename__ = "valoraciones_actividades"

    id = Column(Integer, primary_key=True, autoincrement=True)
    asignacion_id = Column(
        Integer,
        ForeignKey("recursos_tareas.id", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False,
    )
    puntuacion = Column(Integer, nullable=False)
    comentario = Column(Text)
    fecha = Column(DateTime, default=datetime.utcnow)

    asignacion = relationship("RecursoTarea", back_populates="valoraciones")
