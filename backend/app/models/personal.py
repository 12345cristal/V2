# app/models/personal.py

from sqlalchemy import (
    Column, Integer, String, Date, Enum, ForeignKey, Text
)
from sqlalchemy.orm import relationship
from app.db.session import Base
from enum import Enum as PyEnum


# ============================
# ENUM ESTADO LABORAL
# ============================
class EstadoLaboralEnum(str, PyEnum):
    ACTIVO = "ACTIVO"
    VACACIONES = "VACACIONES"
    INACTIVO = "INACTIVO"


# ============================
# MODELO PERSONAL
# ============================
class Personal(Base):
    __tablename__ = "personal"

    id_personal = Column(Integer, primary_key=True, index=True)

    # ------------------------------
    # DATOS BÁSICOS
    # ------------------------------
    nombres = Column(String(100), nullable=False)
    apellido_paterno = Column(String(100), nullable=False)
    apellido_materno = Column(String(100), nullable=True)
    id_rol = Column(Integer, ForeignKey("roles.id_rol"), nullable=False)
    especialidad_principal = Column(String(150), nullable=False)

    # ------------------------------
    # CONTACTO
    # ------------------------------
    telefono_personal = Column(String(20), nullable=False)
    correo_personal = Column(String(150), nullable=False, unique=True)

    # ------------------------------
    # DATOS LABORALES
    # ------------------------------
    fecha_ingreso = Column(Date, nullable=False)
    estado_laboral = Column(Enum(EstadoLaboralEnum), default=EstadoLaboralEnum.ACTIVO)

    # Métricas dashboard
    total_pacientes = Column(Integer, nullable=True)
    sesiones_semana = Column(Integer, nullable=True)
    rating = Column(Integer, nullable=True)

    # ------------------------------
    # DATOS EXTRA
    # ------------------------------
    fecha_nacimiento = Column(Date, nullable=False)
    grado_academico = Column(String(100), nullable=False)
    especialidades = Column(Text, nullable=True)
    rfc = Column(String(20), nullable=False)
    ine = Column(String(30), nullable=False)
    curp = Column(String(20), nullable=False)

    domicilio_calle = Column(String(150), nullable=False)
    domicilio_colonia = Column(String(150), nullable=False)
    domicilio_cp = Column(String(10), nullable=False)
    domicilio_municipio = Column(String(100), nullable=False)
    domicilio_estado = Column(String(100), nullable=False)

    cv_archivo = Column(String(255), nullable=True)
    experiencia = Column(Text, nullable=True)

    # ------------------------------
    # RELACIÓN CON TERAPIA PRINCIPAL
    # ------------------------------
    id_terapia_principal = Column(
        Integer,
        ForeignKey("terapias.id"),  # Ajusta según tu modelo Terapia
        nullable=True
    )

    terapia_principal = relationship("Terapia", back_populates="personal_asignado")

    # ------------------------------
    # RELACIONES
    # ------------------------------
    usuario = relationship("Usuario", back_populates="personal", uselist=False)
    rol = relationship("Rol", back_populates="personal", uselist=False)
    horarios = relationship(
        "HorarioPersonal",
        back_populates="personal",
        cascade="all, delete-orphan"
    )
