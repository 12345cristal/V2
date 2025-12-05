# app/models/tutores.py
from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship

from app.db.base import Base


class Tutor(Base):
    __tablename__ = "tutores"

    id = Column(Integer, primary_key=True, autoincrement=True)
    usuario_id = Column(
        Integer,
        ForeignKey("usuarios.id", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False,
        unique=True,
    )
    ocupacion = Column(String(100))
    notas = Column(Text)

    usuario = relationship("Usuario", back_populates="tutor", lazy="joined")
    direccion = relationship(
        "TutorDireccion", back_populates="tutor", uselist=False
    )
    ninos_principales = relationship(
        "Nino", back_populates="tutor_principal", foreign_keys="Nino.tutor_principal_id"
    )


class TutorDireccion(Base):
    __tablename__ = "tutores_direccion"

    id = Column(Integer, primary_key=True, autoincrement=True)
    tutor_id = Column(
        Integer,
        ForeignKey("tutores.id", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False,
    )
    calle = Column(String(200))
    numero = Column(String(20))
    colonia = Column(String(200))
    municipio = Column(String(100))
    codigo_postal = Column(String(10))

    tutor = relationship("Tutor", back_populates="direccion")
