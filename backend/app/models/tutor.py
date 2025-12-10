# app/models/tutor.py
from sqlalchemy import Column, Integer, String, ForeignKey, Text
from sqlalchemy.orm import relationship
from app.db.base_class import Base


class Tutor(Base):
    """Modelo de Tutores/Padres"""
    __tablename__ = "tutores"

    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id", ondelete="CASCADE"), unique=True, nullable=False)
    ocupacion = Column(String(120))
    notas = Column(Text)

    # Relaciones
    usuario = relationship("Usuario")
    ninos = relationship("Nino", back_populates="tutor")
    direccion = relationship("TutorDireccion", back_populates="tutor", uselist=False, cascade="all, delete-orphan")


class TutorDireccion(Base):
    """Dirección del tutor"""
    __tablename__ = "tutores_direccion"

    id = Column(Integer, primary_key=True, index=True)
    tutor_id = Column(Integer, ForeignKey("tutores.id", ondelete="CASCADE"), nullable=False)
    calle = Column(String(200))
    numero = Column(String(20))
    colonia = Column(String(200))
    municipio = Column(String(100))
    codigo_postal = Column(String(10))

    tutor = relationship("Tutor", back_populates="direccion")
