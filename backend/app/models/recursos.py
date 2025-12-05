from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    SmallInteger,
    Boolean,
    DateTime,
    ForeignKey,
    DECIMAL,
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.base import Base


class RecursoTerapeuta(Base):
    __tablename__ = "recursos_terapeuta"

    id = Column(Integer, primary_key=True, autoincrement=True)
    personal_id = Column(Integer, ForeignKey("personal.id", ondelete="CASCADE"), nullable=False)
    titulo = Column(String(200))
    descripcion = Column(Text)
    tipo_id = Column(SmallInteger, ForeignKey("cat_tipo_recurso.id", ondelete="SET NULL"))
    categoria_id = Column(SmallInteger, ForeignKey("cat_categoria_recurso.id", ondelete="SET NULL"))
    nivel_id = Column(SmallInteger, ForeignKey("cat_nivel_recurso.id", ondelete="SET NULL"))
    etiquetas = Column(Text)
    es_destacado = Column(Boolean, default=False)
    es_nuevo = Column(Boolean, default=True)
    fecha_publicacion = Column(DateTime, server_default=func.current_timestamp())
    ultima_actualizacion = Column(DateTime, server_default=func.current_timestamp())
    total_asignaciones = Column(Integer, default=0)
    total_completadas = Column(Integer, default=0)
    rating_promedio = Column(DECIMAL(3, 2))

    personal = relationship("Personal", back_populates="recursos")
    tareas = relationship("RecursoTarea", back_populates="recurso")


class RecursoTarea(Base):
    __tablename__ = "recursos_tareas"

    id = Column(Integer, primary_key=True, autoincrement=True)
    recurso_id = Column(Integer, ForeignKey("recursos_terapeuta.id", ondelete="CASCADE"), nullable=False)
    nino_id = Column(Integer, ForeignKey("ninos.id", ondelete="CASCADE"), nullable=False)
    tutor_nombre = Column(String(200))
    fecha_asignacion = Column(DateTime, server_default=func.current_timestamp())
    fecha_limite = Column(DateTime)
    completado = Column(Boolean, default=False)
    comentarios_padres = Column(Text)
    notas_terapeuta = Column(Text)

    recurso = relationship("RecursoTerapeuta", back_populates="tareas")
    nino = relationship("Nino", back_populates="recursos_tareas")
    valoraciones = relationship("ValoracionActividad", back_populates="asignacion")


class ValoracionActividad(Base):
    __tablename__ = "valoraciones_actividades"

    id = Column(Integer, primary_key=True, autoincrement=True)
    asignacion_id = Column(Integer, ForeignKey("recursos_tareas.id", ondelete="CASCADE"), nullable=False)
    puntuacion = Column(Integer, nullable=False)
    comentario = Column(Text)
    fecha = Column(DateTime, server_default=func.current_timestamp())

    asignacion = relationship("RecursoTarea", back_populates="valoraciones")
