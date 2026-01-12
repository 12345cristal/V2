# app/models/medicamentos.py
from datetime import datetime
from sqlalchemy import Column, Integer, String, Date, Boolean, DateTime, ForeignKey, Text, Enum
from sqlalchemy.orm import relationship
from app.db.base_class import Base


class Medicamento(Base):
    """Modelo de Medicamentos del niño"""
    __tablename__ = "medicamentos"

    id = Column(Integer, primary_key=True, index=True)
    nino_id = Column(Integer, ForeignKey("ninos.id", ondelete="CASCADE"), nullable=False)
    nombre = Column(String(200), nullable=False)
    dosis = Column(String(100), nullable=False)
    frecuencia = Column(String(100), nullable=False)
    razon = Column(String(255), nullable=False)
    fecha_inicio = Column(Date, nullable=False)
    fecha_fin = Column(Date, nullable=True)
    activo = Column(Boolean, default=True, nullable=False)
    novedadReciente = Column(Boolean, default=False, nullable=False)
    fecha_actualizacion = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    actualizado_por = Column(String(100), nullable=True)
    notas = Column(Text, nullable=True)
    fecha_creacion = Column(DateTime, default=datetime.utcnow)

    # Relaciones
    nino = relationship("Nino", back_populates="medicamentos")


class Alergia(Base):
    """Modelo de Alergias del niño"""
    __tablename__ = "alergias"

    id = Column(Integer, primary_key=True, index=True)
    nino_id = Column(Integer, ForeignKey("ninos.id", ondelete="CASCADE"), nullable=False)
    nombre = Column(String(200), nullable=False)
    severidad = Column(
        Enum("leve", "moderada", "severa", name="severidad_alergia_enum"),
        nullable=False,
        default="leve"
    )
    reaccion = Column(Text, nullable=False)
    tratamiento = Column(Text, nullable=True)
    fecha_registro = Column(DateTime, default=datetime.utcnow)

    # Relaciones
    nino = relationship("Nino", back_populates="alergias")
