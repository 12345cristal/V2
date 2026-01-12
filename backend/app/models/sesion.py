from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum, Text, Boolean, func
from sqlalchemy.orm import relationship
from app.db.base_class import Base
import enum

class EstadoSesion(enum.Enum):
    completada = "completada"
    pendiente = "pendiente"
    cancelada = "cancelada"
reprogramada = "reprogramada"   
class Sesion(Base):
    __tablename__ = "sesiones"
    
    id = Column(Integer, primary_key=True, index=True)
    hijo_id = Column(Integer, ForeignKey("pacientes.id", ondelete="CASCADE"), nullable=False, index=True)
    terapeuta_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    tipo_terapia = Column(String(100), nullable=False)
    fecha = Column(String(10), nullable=False, index=True)
    hora_inicio = Column(String(5), nullable=False)
    hora_fin = Column(String(5), nullable=False)
    estado = Column(Enum(EstadoSesion), default=EstadoSesion.pendiente, nullable=False)
    puntuacion = Column(Integer, nullable=True)
    comentarios = Column(Text, nullable=True)
    grabacion_url = Column(String(500), nullable=True)
    bitacora_url = Column(String(500), nullable=True)
    fecha_creacion = Column(DateTime, server_default=func.now())
    
    hijo = relationship("Paciente", back_populates="sesiones")
    terapeuta = relationship("Usuario", foreign_keys=[terapeuta_id])
    actividades = relationship("ActividadSesion", back_populates="sesion", cascade="all, delete-orphan")

class ActividadSesion(Base):
    __tablename__ = "actividades_sesiones"
    
    id = Column(Integer, primary_key=True, index=True)
    sesion_id = Column(Integer, ForeignKey("sesiones.id", ondelete="CASCADE"), nullable=False)
    nombre = Column(String(255), nullable=False)
    descripcion = Column(Text, nullable=True)
    completada = Column(Boolean, default=False)
    observaciones = Column(Text, nullable=True)
    
    sesion = relationship("Sesion", back_populates="actividades")