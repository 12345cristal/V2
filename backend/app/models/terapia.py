# app/models/terapia.py

from sqlalchemy import Column, Integer, String, Text, Enum, ForeignKey
from sqlalchemy.orm import relationship
from app.db.session import Base


# ============================
# ENUM PARA ESTADO DE TERAPIA
# ============================
class EstadoTerapiaEnum(str, Enum):
    ACTIVA = "ACTIVA"
    INACTIVA = "INACTIVA"


# ============================
# MODELO TERAPIA
# ============================
class Terapia(Base):
    __tablename__ = "terapias"

    id_terapia = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(150), nullable=False, unique=True)
    descripcion = Column(Text, nullable=False)
    estado = Column(Enum(EstadoTerapiaEnum), default=EstadoTerapiaEnum.ACTIVA)

    # Relación con asignaciones (muchos asignados)
    asignaciones = relationship(
        "AsignacionTerapia",
        back_populates="terapia",
        cascade="all, delete-orphan"
    )


# ============================
# MODELO ASIGNACIÓN TERAPIA
# ============================
class AsignacionTerapia(Base):
    __tablename__ = "asignaciones_terapia"

    id_asignacion = Column(Integer, primary_key=True, index=True)
    id_personal = Column(Integer, ForeignKey("personal.id_personal"), nullable=False)
    id_terapia = Column(Integer, ForeignKey("terapias.id_terapia"), nullable=False)

    personal = relationship("Personal", back_populates="asignaciones_terapias")
    terapia = relationship("Terapia", back_populates="asignaciones")
