# app/models/terapia.py

from sqlalchemy import Column, Integer, String, Text, Enum, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from enum import Enum as PyEnum

from app.db.base import Base  # Base de SQLAlchemy para todos los modelos


# =============================================================
# ENUM: Estado de la Terapia
# =============================================================
class EstadoTerapiaEnum(str, PyEnum):
    """
    Enum que define el estado de una terapia.
    """
    ACTIVA = "ACTIVA"
    INACTIVA = "INACTIVA"


# =============================================================
# MODELO: Terapia
# =============================================================
class Terapia(Base):
    """
    Representa un tipo de terapia dentro del sistema.
    """

    __tablename__ = "terapias"

    id_terapia = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(150), nullable=False, unique=True)
    descripcion = Column(Text, nullable=True)
    estado = Column(
        Enum(EstadoTerapiaEnum),
        default=EstadoTerapiaEnum.ACTIVA,
        nullable=False
    )

    # ---------------------------------------------------------
    # RELACIONES
    # ---------------------------------------------------------

    # Asignaciones múltiples (relación N:N con Personal)
    asignaciones = relationship(
        "AsignacionTerapia",
        back_populates="terapia",
        cascade="all, delete-orphan"
    )

    # Personal que tiene esta terapia como principal
    personal_asignado = relationship(
        "Personal",
        back_populates="terapia_principal"
    )


# =============================================================
# MODELO: AsignacionTerapia
# =============================================================
class AsignacionTerapia(Base):
    """
    Representa la asignación de un personal a una terapia.
    Permite definir si la terapia es principal para el personal.
    """

    __tablename__ = "asignaciones_terapia"

    id_asignacion = Column(Integer, primary_key=True, index=True)
    id_personal = Column(Integer, ForeignKey("personal.id_personal"), nullable=False)
    id_terapia = Column(Integer, ForeignKey("terapias.id_terapia"), nullable=False)
    es_principal = Column(Boolean, default=True, nullable=False)

    # ---------------------------------------------------------
    # RELACIONES
    # ---------------------------------------------------------
    personal = relationship(
        "Personal",
        back_populates="asignaciones_terapia"
    )

    terapia = relationship(
        "Terapia",
        back_populates="asignaciones"
    )
