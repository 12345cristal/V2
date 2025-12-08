# app/models/tutor.py
"""Modelos para Tutores/Padres"""

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base_class import Base


class Tutor(Base):
    __tablename__ = "tutores"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id", ondelete="CASCADE"), nullable=False, unique=True)
    ocupacion = Column(String(120))
    notas = Column(String)  # TEXT
    
    # Relationships
    usuario = relationship("Usuario", back_populates="tutor")
    direcciones = relationship("TutorDireccion", back_populates="tutor")
    ninos = relationship("Nino", back_populates="tutor")


class TutorDireccion(Base):
    __tablename__ = "tutores_direccion"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    tutor_id = Column(Integer, ForeignKey("tutores.id", ondelete="CASCADE"), nullable=False)
    calle = Column(String(200))
    numero = Column(String(20))
    colonia = Column(String(200))
    municipio = Column(String(100))
    codigo_postal = Column(String(10))
    
    # Relationships
    tutor = relationship("Tutor", back_populates="direcciones")
