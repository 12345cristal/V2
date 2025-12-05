from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    Date,
    Time,
    Boolean,
    SmallInteger,
    ForeignKey,
)
from sqlalchemy.orm import relationship
from app.db.base import Base


class Cita(Base):
    __tablename__ = "citas"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nino_id = Column(Integer, ForeignKey("ninos.id", ondelete="SET NULL"))
    es_nuevo_nino = Column(Boolean, nullable=False, default=False)
    temp_nino_nombre = Column(String(100))
    temp_nino_apellido_paterno = Column(String(50))
    temp_nino_apellido_materno = Column(String(50))
    temp_tutor_nombre = Column(String(100))
    temp_tutor_apellido_paterno = Column(String(50))
    temp_tutor_apellido_materno = Column(String(50))
    telefono_temporal = Column(String(20))
    terapeuta_id = Column(Integer, ForeignKey("personal.id", ondelete="SET NULL"))
    terapia_id = Column(Integer, ForeignKey("terapias.id", ondelete="SET NULL"))
    fecha = Column(Date, nullable=False)
    hora_inicio = Column(Time, nullable=False)
    hora_fin = Column(Time, nullable=False)
    estado_id = Column(SmallInteger, ForeignKey("cat_estado_cita.id", ondelete="RESTRICT"), nullable=False)
    es_reposicion = Column(Boolean, nullable=False, default=False)
    motivo = Column(Text)
    diagnostico_presuntivo = Column(String(255))
    observaciones = Column(Text)

    nino = relationship("Nino", back_populates="citas")
    terapeuta = relationship("Personal", back_populates="citas")
    terapia = relationship("Terapia")
    observadores = relationship("CitaObservador", back_populates="cita")


class CitaObservador(Base):
    __tablename__ = "citas_observadores"

    id = Column(Integer, primary_key=True, autoincrement=True)
    cita_id = Column(Integer, ForeignKey("citas.id", ondelete="CASCADE"), nullable=False)
    terapeuta_id = Column(Integer, ForeignKey("personal.id", ondelete="CASCADE"), nullable=False)

    cita = relationship("Cita", back_populates="observadores")
    terapeuta = relationship("Personal")
