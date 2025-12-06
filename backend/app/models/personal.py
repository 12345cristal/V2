# app/models/personal.py

from sqlalchemy import (
    Column, Integer, String, Date, Enum, ForeignKey, Float, Text
)
from sqlalchemy.orm import relationship
from enum import Enum as PyEnum

from app.db.base_class import Base  # Base común para todos los modelos


# =============================================================
# ENUM: Estado laboral del personal
# =============================================================
class EstadoLaboralEnum(str, PyEnum):
    ACTIVO = "ACTIVO"
    VACACIONES = "VACACIONES"
    INACTIVO = "INACTIVO"


# =============================================================
# MODELO: Personal
# =============================================================
class Personal(Base):
    """
    Representa a un miembro del personal dentro del sistema.
    Incluye datos personales, dirección, documentos, datos profesionales,
    métricas de desempeño y relaciones con roles y terapias.
    """

    __tablename__ = "personal"

    id_personal = Column(Integer, primary_key=True, index=True)

    # ---------------------------------------------------------
    # DATOS PERSONALES
    # ---------------------------------------------------------
    nombres = Column(String(100), nullable=False)
    apellido_paterno = Column(String(100), nullable=False)
    apellido_materno = Column(String(100), nullable=True)
    fecha_nacimiento = Column(Date, nullable=False)
    telefono_personal = Column(String(20), nullable=False)
    correo_personal = Column(String(150), nullable=False, unique=True)

    # ---------------------------------------------------------
    # IDENTIDAD Y DOCUMENTOS
    # ---------------------------------------------------------
    rfc = Column(String(20), nullable=False)
    ine = Column(String(30), nullable=False)
    curp = Column(String(20), nullable=False)

    # ---------------------------------------------------------
    # DIRECCIÓN
    # ---------------------------------------------------------
    domicilio_calle = Column(String(150), nullable=False)
    domicilio_colonia = Column(String(150), nullable=False)
    domicilio_cp = Column(String(10), nullable=False)
    domicilio_municipio = Column(String(100), nullable=False)
    domicilio_estado = Column(String(100), nullable=False)

    # ---------------------------------------------------------
    # DATOS PROFESIONALES
    # ---------------------------------------------------------
    grado_academico = Column(String(100), nullable=False)
    especialidad_principal = Column(String(150), nullable=False)
    especialidades = Column(Text, nullable=True)
    experiencia = Column(Text, nullable=True)
    cv_archivo = Column(String(255), nullable=True)

    fecha_ingreso = Column(Date, nullable=False)
    estado_laboral = Column(
        Enum(EstadoLaboralEnum),
        default=EstadoLaboralEnum.ACTIVO,
        nullable=False
    )

    # ---------------------------------------------------------
    # RELACIÓN CON ROL DEL SISTEMA
    # ---------------------------------------------------------
    id_rol = Column(Integer, ForeignKey("roles.id_rol"), nullable=False)
    rol = relationship("Rol", back_populates="personal")

    # ---------------------------------------------------------
    # TERAPIA PRINCIPAL ASIGNADA
    # ---------------------------------------------------------
    id_terapia_principal = Column(Integer, ForeignKey("terapias.id_terapia"), nullable=True)
    terapia_principal = relationship("Terapia", back_populates="personal_asignado", foreign_keys=[id_terapia_principal])

    # Relación N:N con terapias asignadas
    asignaciones_terapia = relationship("AsignacionTerapia", back_populates="personal")

    # ---------------------------------------------------------
    # MÉTRICAS PARA DASHBOARD / TOPSIS
    # ---------------------------------------------------------
    total_pacientes = Column(Integer, nullable=True)
    sesiones_semana = Column(Integer, nullable=True)
    rating = Column(Float, nullable=True)

    # ---------------------------------------------------------
    # RELACIONES ADICIONALES
    # ---------------------------------------------------------
    usuario = relationship("Usuario", back_populates="personal", uselist=False)

    horarios = relationship(
        "HorarioPersonal",
        back_populates="personal",
        cascade="all, delete-orphan"
    )
