from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    SmallInteger,
    Boolean,
    DateTime,
    ForeignKey,
    Enum as SAEnum,
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.base import Base


class Terapia(Base):
    __tablename__ = "terapias"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(60), nullable=False)
    descripcion = Column(Text)
    tipo_terapia_id = Column(SmallInteger, ForeignKey("cat_tipo_terapia.id", ondelete="RESTRICT", onupdate="CASCADE"), nullable=False)
    duracion_minutos = Column(Integer, nullable=False)
    objetivo_general = Column(Text, nullable=False)
    activo = Column(Boolean, nullable=False, default=True)

    personal_terapias = relationship("PersonalTerapia", back_populates="terapia")
    terapias_nino = relationship("TerapiaNino", back_populates="terapia")
    sesiones = relationship("SesionTerapia", secondary="terapias_nino")


class PersonalTerapia(Base):
    __tablename__ = "personal_terapias"

    id = Column(Integer, primary_key=True, autoincrement=True)
    personal_id = Column(Integer, ForeignKey("personal.id", ondelete="CASCADE"), nullable=False)
    terapia_id = Column(Integer, ForeignKey("terapias.id", ondelete="CASCADE"), nullable=False)

    personal = relationship("Personal", back_populates="terapias")
    terapia = relationship("Terapia", back_populates="personal_terapias")


class TerapiaNino(Base):
    __tablename__ = "terapias_nino"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nino_id = Column(Integer, ForeignKey("ninos.id", ondelete="CASCADE"), nullable=False)
    terapia_id = Column(Integer, ForeignKey("terapias.id", ondelete="CASCADE"), nullable=False)
    terapeuta_id = Column(Integer, ForeignKey("personal.id", ondelete="SET NULL"))
    fecha_asignacion = Column(DateTime, nullable=False, server_default=func.current_timestamp())
    frecuencia_semana = Column(Integer, nullable=False)
    prioridad_id = Column(SmallInteger, ForeignKey("cat_prioridad.id", ondelete="RESTRICT"), nullable=False)
    activo = Column(Boolean, nullable=False, default=True)

    nino = relationship("Nino", back_populates="terapias_nino")
    terapia = relationship("Terapia", back_populates="terapias_nino")
    terapeuta = relationship("Personal", back_populates="terapias_nino")
    sesiones = relationship("SesionTerapia", back_populates="terapia_nino")


class SesionTerapia(Base):
    __tablename__ = "sesiones_terapia"

    id = Column(Integer, primary_key=True, autoincrement=True)
    terapia_nino_id = Column(Integer, ForeignKey("terapias_nino.id", ondelete="CASCADE"), nullable=False)
    fecha_sesion = Column(DateTime, nullable=False, server_default=func.current_timestamp())
    asistio = Column(Boolean, nullable=False, default=True)
    nivel_progreso = Column(Integer, nullable=False, default=0)
    nivel_colaboracion = Column(Integer, nullable=False, default=0)
    observaciones = Column(Text)
    creado_por_id = Column(Integer, ForeignKey("personal.id", ondelete="SET NULL"))

    terapia_nino = relationship("TerapiaNino", back_populates="sesiones")
    creado_por = relationship("Personal", back_populates="sesiones_creadas")


class ReposicionTerapia(Base):
    __tablename__ = "reposiciones_terapia"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nino_id = Column(Integer, ForeignKey("ninos.id", ondelete="CASCADE"), nullable=False)
    terapia_id = Column(Integer, ForeignKey("terapias.id", ondelete="CASCADE"), nullable=False)
    fecha_original = Column(DateTime, nullable=False)
    fecha_nueva = Column(DateTime, nullable=False)
    motivo = Column(Text)
    estado = Column(
        SAEnum("PENDIENTE", "APROBADA", "RECHAZADA", name="estado_reposicion_enum"),
        default="PENDIENTE",
    )

    nino = relationship("Nino")
    terapia = relationship("Terapia")
