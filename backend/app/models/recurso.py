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
# ENUMS
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
# MODELO RECURSO
# ============================

class Recurso(Base):
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

    fecha_creacion = Column(DateTime, default=datetime.utcnow)

    # =========================
    # FK
    # =========================
    terapeuta_id = Column(
        Integer,
        ForeignKey("personal.id", ondelete="CASCADE"),
        nullable=False,
    )

    # =========================
    # RELACIONES
    # =========================
    terapeuta = relationship(
        "Personal",
        back_populates="recursos",
    )

    recomendaciones = relationship(
        "Recomendacion",
        back_populates="recurso",
        cascade="all, delete-orphan",
    )

    vistas = relationship(
        "RecursoVisto",
        back_populates="recurso",
        cascade="all, delete-orphan",
    )


# ============================
# RECOMENDACIÓN DE RECURSO
# ============================

class Recomendacion(Base):
    __tablename__ = "recomendaciones"

    id = Column(Integer, primary_key=True, index=True)

    recurso_id = Column(
        Integer,
        ForeignKey("recursos.id", ondelete="CASCADE"),
        nullable=False,
    )

    nino_id = Column(
        Integer,
        ForeignKey("ninos.id", ondelete="CASCADE"),
        nullable=False,
    )

    terapeuta_id = Column(
        Integer,
        ForeignKey("personal.id", ondelete="CASCADE"),
        nullable=False,
    )

    fecha_recomendacion = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )

    # =========================
    # RELACIONES
    # =========================
    recurso = relationship(
        "Recurso",
        back_populates="recomendaciones",
    )

    nino = relationship("Nino")

    terapeuta = relationship("Personal")


# ============================
# RECURSO VISTO
# ============================

class RecursoVisto(Base):
    __tablename__ = "recursos_vistos"

    id = Column(Integer, primary_key=True, index=True)

    recurso_id = Column(
        Integer,
        ForeignKey("recursos.id", ondelete="CASCADE"),
        nullable=False,
    )

    usuario_id = Column(
        Integer,
        ForeignKey("usuarios.id", ondelete="CASCADE"),
        nullable=False,
    )

    fecha_visto = Column(DateTime, default=datetime.utcnow)

    __table_args__ = (
        UniqueConstraint(
            "recurso_id",
            "usuario_id",
            name="uq_recurso_usuario",
        ),
    )

    # =========================
    # RELACIONES
    # =========================
    recurso = relationship(
        "Recurso",
        back_populates="vistas",
    )

    usuario = relationship(
        "Usuario",
        back_populates="recursos_vistos",
    )
