# app/models/personal.py
"""Modelos para Personal (Terapeutas y staff)"""

from sqlalchemy import Column, Integer, String, ForeignKey, Date, SmallInteger, DECIMAL
from sqlalchemy.orm import relationship
from app.db.base_class import Base


class Personal(Base):
    __tablename__ = "personal"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id", ondelete="CASCADE"), nullable=False, unique=True)
    especialidad_principal = Column(String(120))
    fecha_ingreso = Column(Date)
    estado_laboral_id = Column(SmallInteger, ForeignKey("estado_laboral.id", ondelete="SET NULL"))
    total_pacientes = Column(Integer, default=0)
    sesiones_semana = Column(Integer, default=0)
    rating = Column(DECIMAL(3, 2))
    
    # Relationships
    usuario = relationship("Usuario", back_populates="personal")
    estado_laboral = relationship("EstadoLaboral", back_populates="personal")
    perfil = relationship("PersonalPerfil", back_populates="personal", uselist=False)
    horarios = relationship("PersonalHorario", back_populates="personal")
    terapias_asignadas = relationship("TerapiaPersonal", back_populates="personal")
    terapias_nino = relationship("TerapiaNino", back_populates="terapeuta")
    sesiones_creadas = relationship("Sesion", back_populates="creado_por_personal")
    citas_terapeuta = relationship("Cita", back_populates="terapeuta")
    recursos = relationship("Recurso", back_populates="personal")
    tareas_asignadas = relationship("TareaRecurso", back_populates="asignado_por_personal")


class PersonalPerfil(Base):
    __tablename__ = "personal_perfil"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    personal_id = Column(Integer, ForeignKey("personal.id", ondelete="CASCADE"), nullable=False, unique=True)
    fecha_nacimiento = Column(Date)
    grado_academico_id = Column(SmallInteger, ForeignKey("grado_academico.id", ondelete="SET NULL"))
    especialidades = Column(String)  # TEXT en MySQL
    rfc = Column(String(13))
    ine = Column(String(18))
    curp = Column(String(18))
    telefono_personal = Column(String(20))
    correo_personal = Column(String(100))
    domicilio_calle = Column(String(100))
    domicilio_colonia = Column(String(100))
    domicilio_cp = Column(String(10))
    domicilio_municipio = Column(String(100))
    domicilio_estado = Column(String(100))
    cv_url = Column(String(255))
    experiencia = Column(String)  # TEXT
    
    # Relationships
    personal = relationship("Personal", back_populates="perfil")
    grado_academico = relationship("GradoAcademico", back_populates="personal_perfiles")


class PersonalHorario(Base):
    __tablename__ = "personal_horarios"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    personal_id = Column(Integer, ForeignKey("personal.id", ondelete="CASCADE"), nullable=False)
    dia_semana = Column(SmallInteger, nullable=False)  # 0=Lunes, 6=Domingo
    hora_inicio = Column(String(8), nullable=False)  # TIME en formato HH:MM:SS
    hora_fin = Column(String(8), nullable=False)
    
    # Relationships
    personal = relationship("Personal", back_populates="horarios")
