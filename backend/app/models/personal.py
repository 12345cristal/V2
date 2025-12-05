# app/models/personal.py
from sqlalchemy import (
    Column,
    Integer,
    String,
    Enum,
    ForeignKey,
)
from sqlalchemy.orm import relationship

from app.db.base import Base


CEDULA_ESTATUS_ENUM = ("VALIDA", "EN_TRAMITE", "NO_APLICA")


class Personal(Base):
    __tablename__ = "personal"

    id = Column(Integer, primary_key=True, autoincrement=True)
    usuario_id = Column(
        Integer,
        ForeignKey("usuarios.id", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False,
        unique=True,
    )
    rol_id = Column(
        Integer,
        ForeignKey("roles.id", ondelete="RESTRICT", onupdate="CASCADE"),
        nullable=False,
    )
    cedula_profesional = Column(String(20))
    cedula_estatus = Column(
        Enum(*CEDULA_ESTATUS_ENUM, name="cedula_estatus_enum"),
        nullable=False,
        default="NO_APLICA",
    )
    especialidad = Column(String(100))
    anio_experiencia = Column(Integer, default=0)

    usuario = relationship("Usuario", back_populates="personal", lazy="joined")
    rol = relationship("Rol", lazy="joined")
    terapias = relationship("PersonalTerapia", back_populates="personal")
