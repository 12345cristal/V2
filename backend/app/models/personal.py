# backend/app/models/personal.py
from sqlalchemy import Column, Integer, String, Date, ForeignKey, SmallInteger, Time, Enum as SQLEnum
from sqlalchemy.orm import relationship
from app.db.base_class import Base
import enum


class EstadoLaboral(str, enum.Enum):
    ACTIVO = "ACTIVO"
    VACACIONES = "VACACIONES"
    INACTIVO = "INACTIVO"


class Personal(Base):
    __tablename__ = "personal"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombres = Column(String(100), nullable=False)
    apellido_paterno = Column(String(100), nullable=False)
    apellido_materno = Column(String(100))
    
    # Relación con usuario
    id_usuario = Column(Integer, ForeignKey("usuarios.id"))
    
    # Rol (terapeuta, coordinador, etc.)
    id_rol = Column(Integer, ForeignKey("roles.id"), nullable=False)
    rol = relationship("Rol", back_populates="personal")
    
    # Información personal
    rfc = Column(String(13), unique=True, nullable=False)
    curp = Column(String(18), unique=True, nullable=False)
    fecha_nacimiento = Column(Date, nullable=False)
    
    # Contacto
    telefono_personal = Column(String(10), nullable=False)
    correo_personal = Column(String(150), unique=True, nullable=False)
    
    # Domicilio
    calle = Column(String(200))
    numero_exterior = Column(String(10))
    numero_interior = Column(String(10))
    colonia = Column(String(100))
    ciudad = Column(String(100))
    estado = Column(String(100))
    codigo_postal = Column(String(5))
    
    # Información profesional
    especialidad_principal = Column(String(100))
    especialidades = Column(String(500))  # JSON string con múltiples especialidades
    grado_academico = Column(String(100))
    cedula_profesional = Column(String(20))
    
    # Información laboral
    fecha_ingreso = Column(Date, nullable=False)
    estado_laboral = Column(SQLEnum(EstadoLaboral), default=EstadoLaboral.ACTIVO, nullable=False)
    experiencia = Column(Integer, default=0)  # años de experiencia
    
    # Métricas
    total_pacientes = Column(Integer, default=0)
    sesiones_semana = Column(Integer, default=0)
    rating = Column(Integer, default=0)  # 0-5 estrellas
    
    # Relaciones
    horarios = relationship("PersonalHorario", back_populates="personal", cascade="all, delete-orphan")
    usuario = relationship("Usuario", back_populates="personal", uselist=False)
    terapias_asignadas = relationship("TerapiaPersonal", back_populates="personal", cascade="all, delete-orphan")


class PersonalHorario(Base):
    __tablename__ = "personal_horario"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    id_personal = Column(Integer, ForeignKey("personal.id", ondelete="CASCADE"), nullable=False)
    dia_semana = Column(SmallInteger, nullable=False)  # 1=Lunes, 7=Domingo
    hora_inicio = Column(Time, nullable=False)
    hora_fin = Column(Time, nullable=False)
    
    personal = relationship("Personal", back_populates="horarios")
