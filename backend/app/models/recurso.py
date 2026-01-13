from datetime import datetime
from enum import Enum

from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    DateTime,
    ForeignKey,
    UniqueConstraint,
    Enum as SQLEnum,
)
from sqlalchemy.orm import relationship

from app.db.base_class import Base


# ============================
# ENUMS (CATÁLOGOS)
# ============================

class TipoRecurso(str, Enum):
    PDF = "PDF"
    VIDEO = "VIDEO"
    ENLACE = "ENLACE"


class CategoriaRecurso(str, Enum):
    COMUNICACION = "COMUNICACION"
    CONDUCTA = "CONDUCTA"
    SENSORIAL = "SENSORIAL"
    SOCIAL = "SOCIAL"
    COGNITIVO = "COGNITIVO"


class NivelRecurso(str, Enum):
    BASICO = "BASICO"
    INTERMEDIO = "INTERMEDIO"
    AVANZADO = "AVANZADO"


# ============================
# MODELOS
# ============================

class Recurso(Base):
    """Recursos terapéuticos creados por personal"""

    __tablename__ = "recursos"

    id = Column(Integer, primary_key=True, index=True)

    titulo = Column(String(255), nullable=False)
    descripcion = Column(Text)

    tipo_recurso = Column(SQLEnum(TipoRecurso), nullable=False)
    categoria_recurso = Column(SQLEnum(CategoriaRecurso))
    nivel_recurso = Column(SQLEnum(NivelRecurso))

    url = Column(String(500))
    archivo = Column(String(500))
    objetivo_terapeutico = Column(Text)

    terapeuta_id = Column(Integer, ForeignKey("personal.id"))
    fecha_creacion = Column(DateTime, default=datetime.utcnow)

    terapeuta = relationship("Personal", back_populates="recursos")
    recomendaciones = relationship(
        "Recomendacion",
        back_populates="recurso",
        cascade="all, delete-orphan"
    )

    terapeuta_id = Column(Integer, ForeignKey("personal.id"), nullable=False)

class Recomendacion(Base):
    __tablename__ = "recomendaciones"

    id = Column(Integer, primary_key=True, index=True)
    recurso_id = Column(Integer, ForeignKey("recursos.id"), nullable=False)
    nino_id = Column(Integer, ForeignKey("nino.id"), nullable=False)
    terapeuta_id = Column(Integer, ForeignKey("personal.id"), nullable=False)

    fecha_recomendacion = Column(DateTime, default=datetime.utcnow)

    recurso = relationship("Recurso", back_populates="recomendaciones")
    nino = relationship("Nino")
    terapeuta = relationship("Personal")

    # =========================
    # Relaciones
    # =========================
    terapeuta = relationship("Personal", back_populates="recursos")

class RecursoVisto(Base):
    __tablename__ = "recursos_vistos"

    id = Column(Integer, primary_key=True, index=True)
    recurso_id = Column(Integer, ForeignKey("recursos.id"), nullable=False)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    fecha_visto = Column(DateTime, default=datetime.utcnow)

    __table_args__ = (
        UniqueConstraint("recurso_id", "usuario_id", name="uq_recurso_usuario"),
    )
