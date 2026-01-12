from sqlalchemy import Column, Integer, String, Date, DateTime, ForeignKey, Boolean, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.base_class import Base

class Paciente(Base):
    __tablename__ = "pacientes"
    
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    edad = Column(Integer, nullable=True)
    fecha_nacimiento = Column(Date, nullable=True)
    diagnostico = Column(String(255), nullable=True)
    avatar = Column(String(500), nullable=True)
    descripcion = Column(Text, nullable=True)
    estado = Column(Boolean, default=True, nullable=False)
    fecha_creacion = Column(DateTime, server_default=func.now())
    fecha_actualizacion = Column(DateTime, onupdate=func.now())
    
    # Nuevas relaciones
    tareas = relationship("Tarea", back_populates="hijo", cascade="all, delete-orphan")
    notificaciones = relationship("Notificacion", foreign_keys="Notificacion.hijo_id")
    sesiones = relationship("Sesion", back_populates="hijo", cascade="all, delete-orphan")
    historial = relationship("Historial", back_populates="hijo", uselist=False, cascade="all, delete-orphan")
    pagos = relationship("Pago", back_populates="hijo", cascade="all, delete-orphan")