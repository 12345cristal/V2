from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    SmallInteger,
    ForeignKey,
    Enum as SAEnum,
    DateTime,
    Float,
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.base import Base


class Actividad(Base):
    __tablename__ = "actividades"

    id = Column(Integer, primary_key=True, autoincrement=True)
    titulo = Column(String(150), nullable=False)
    descripcion = Column(Text, nullable=False)
    edad_min = Column(Integer, nullable=False)
    edad_max = Column(Integer, nullable=False)
    tipo_terapia_id = Column(SmallInteger, ForeignKey("cat_tipo_terapia.id", ondelete="RESTRICT", onupdate="CASCADE"), nullable=False)
    nivel_dificultad_id = Column(SmallInteger, ForeignKey("cat_nivel_dificultad.id", ondelete="RESTRICT", onupdate="CASCADE"), nullable=False)
    materiales = Column(Text)
    etiquetas = Column(Text)

    recomendaciones = relationship("RecomendacionActividad", back_populates="actividad")


class RecomendacionActividad(Base):
    __tablename__ = "recomendaciones_actividades"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nino_id = Column(Integer, ForeignKey("ninos.id", ondelete="CASCADE"), nullable=False)
    actividad_id = Column(Integer, ForeignKey("actividades.id", ondelete="CASCADE"), nullable=False)
    fuente = Column(SAEnum("CONTENT_BASED", "MANUAL", name="fuente_recomendacion_enum"), nullable=False)
    puntaje = Column(Float, nullable=False)
    fecha_generada = Column(DateTime, nullable=False, server_default=func.current_timestamp())

    nino = relationship("Nino", back_populates="recomendaciones_actividades")
    actividad = relationship("Actividad", back_populates="recomendaciones")
