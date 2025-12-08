# app/models/cita.py
"""Modelo para Citas"""

from sqlalchemy import Column, Integer, String, ForeignKey, Date, SmallInteger
from sqlalchemy.orm import relationship
from app.db.base_class import Base


class Cita(Base):
    __tablename__ = "citas"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    nino_id = Column(Integer, ForeignKey("ninos.id", ondelete="SET NULL"))
    terapeuta_id = Column(Integer, ForeignKey("personal.id", ondelete="SET NULL"))
    terapia_id = Column(Integer, ForeignKey("terapias.id", ondelete="SET NULL"))
    fecha = Column(Date, nullable=False)
    hora_inicio = Column(String(8), nullable=False)  # TIME
    hora_fin = Column(String(8), nullable=False)  # TIME
    estado_id = Column(SmallInteger, ForeignKey("estado_cita.id"), nullable=False)
    motivo = Column(String)  # TEXT
    observaciones = Column(String)  # TEXT
    es_reposicion = Column(SmallInteger, default=0)
    
    # Relationships
    nino = relationship("Nino", back_populates="citas")
    terapeuta = relationship("Personal", back_populates="citas_terapeuta")
    terapia = relationship("Terapia", back_populates="citas")
    estado = relationship("EstadoCita", back_populates="citas")
