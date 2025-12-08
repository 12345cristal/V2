# app/models/cita.py
from sqlalchemy import Column, Integer, String, Text, ForeignKey, Date, Time, SmallInteger
from sqlalchemy.orm import relationship
from app.db.base_class import Base


class EstadoCita(Base):
    """
    Catálogo de estados de citas
    """
    __tablename__ = "estado_cita"

    id = Column(SmallInteger, primary_key=True, autoincrement=True)
    codigo = Column(String(30), nullable=False, unique=True)
    nombre = Column(String(80), nullable=False)


class Cita(Base):
    """
    Modelo para la tabla 'citas'
    Representa las citas programadas entre niños y terapeutas
    """
    __tablename__ = "citas"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nino_id = Column(Integer, ForeignKey("ninos.id", ondelete="SET NULL"))
    terapeuta_id = Column(Integer, ForeignKey("personal.id", ondelete="SET NULL"))
    terapia_id = Column(Integer, ForeignKey("terapias.id", ondelete="SET NULL"))
    fecha = Column(Date, nullable=False)
    hora_inicio = Column(Time, nullable=False)
    hora_fin = Column(Time, nullable=False)
    estado_id = Column(SmallInteger, ForeignKey("estado_cita.id"), nullable=False)
    motivo = Column(Text)
    observaciones = Column(Text)
    es_reposicion = Column(SmallInteger, default=0)

    # Relaciones
    nino = relationship("Nino", foreign_keys=[nino_id])
    terapeuta = relationship("Personal", foreign_keys=[terapeuta_id])
    terapia = relationship("Terapia", foreign_keys=[terapia_id])
    estado = relationship("EstadoCita", foreign_keys=[estado_id])
