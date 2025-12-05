# app/models/terapias.py
from datetime import datetime

from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    ForeignKey,
    DateTime,
    SmallInteger,
    Boolean,
    Enum,
)
from sqlalchemy.orm import relationship

from app.db.base import Base


REPOSICION_ESTADO_ENUM = ("PENDIENTE", "APROBADA", "RECHAZADA")


class Terapia(Base):
    __tablename__ = "terapias"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(60), nullable=False)
    descripcion = Column(Text)
    tipo_terapia_id = Column(
        SmallInteger,
        ForeignKey("cat_tipo_terapia.id", ondelete="RESTRICT", onupdate="CASCADE"),
        nullable=False,
    )
    duracion_minutos = Column(Integer, nullable=False)
    objetivo_general = Column(Text, nullable=False)
    activo = Column(Boolean, nullable=False, default=True)

    tipo_terapia = relationship("CatTipoTerapia", lazy="joined")
    personal_terapias = relationship("PersonalTerapia", back_populates="terapia")
    terapias_nino = relationship("TerapiaNino", back_populates="terapia")
    citas = relationship("Cita", back_populates="terapia")


class PersonalTerapia(Base):
    __tablename__ = "personal_terapias"

    id = Column(Integer, primary_key=True, autoincrement=True)
    personal_id = Column(
        Integer,
        ForeignKey("personal.id", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False,
    )
    terapia_id = Column(
        Integer,
        ForeignKey("terapias.id", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False,
    )

    personal = relationship("Personal", back_populates="terapias")
    terapia = relationship("Terapia", back_populates="personal_terapias")


class TerapiaNino(Base):
    __tablename__ = "terapias_nino"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nino_id = Column(
        Integer,
        ForeignKey("ninos.id", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False,
    )
    terapia_id = Column(
        Integer,
        ForeignKey("terapias.id", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False,
    )
    terapeuta_id = Column(
        Integer,
        ForeignKey("personal.id", ondelete="SET NULL", onupdate="CASCADE"),
        nullable=True,
    )
    fecha_asignacion = Column(DateTime, nullable=False, default=datetime.utcnow)
    frecuencia_semana = Column(Integer, nullable=False)
    prioridad_id = Column(
        SmallInteger,
        ForeignKey("cat_prioridad.id", ondelete="RESTRICT", onupdate="CASCADE"),
        nullable=False,
    )
    activo = Column(Boolean, nullable=False, default=True)

    nino = relationship("Nino", back_populates="terapias_nino")
    terapia = relationship("Terapia", back_populates="terapias_nino")
    terapeuta = relationship("Personal")
    prioridad = relationship("CatPrioridad")
    sesiones = relationship("SesionTerapia", back_populates="terapia_nino")


class SesionTerapia(Base):
    __tablename__ = "sesiones_terapia"

    id = Column(Integer, primary_key=True, autoincrement=True)
    terapia_nino_id = Column(
        Integer,
        ForeignKey("terapias_nino.id", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False,
    )
    fecha_sesion = Column(DateTime, nullable=False, default=datetime.utcnow)
    asistio = Column(Boolean, nullable=False, default=True)
    nivel_progreso = Column(Integer, nullable=False, default=0)
    nivel_colaboracion = Column(Integer, nullable=False, default=0)
    observaciones = Column(Text)
    creado_por_id = Column(
        Integer,
        ForeignKey("personal.id", ondelete="SET NULL", onupdate="CASCADE"),
    )

    terapia_nino = relationship("TerapiaNino", back_populates="sesiones")
    creado_por = relationship("Personal")


class ReposicionTerapia(Base):
    __tablename__ = "reposiciones_terapia"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nino_id = Column(
        Integer,
        ForeignKey("ninos.id", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False,
    )
    terapia_id = Column(
        Integer,
        ForeignKey("terapias.id", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False,
    )
    fecha_original = Column(DateTime, nullable=False)
    fecha_nueva = Column(DateTime, nullable=False)
    motivo = Column(Text)
    estado = Column(
        Enum(*REPOSICION_ESTADO_ENUM, name="reposicion_estado_enum"),
        default="PENDIENTE",
    )

    nino = relationship("Nino")
    terapia = relationship("Terapia")
