from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text, Date, func
from sqlalchemy.orm import relationship
from app.db.base_class import Base

class Historial(Base):
    __tablename__ = "historiales"
    
    id = Column(Integer, primary_key=True, index=True)
    hijo_id = Column(Integer, ForeignKey("pacientes.id", ondelete="CASCADE"), nullable=False, unique=True)
    fecha_inicio_terapia = Column(Date, nullable=False)
    duracion_promedio_sesion = Column(Integer, default=50)
    evaluacion_general = Column(Integer, default=0)
    terapeuta_responsable = Column(String(255), nullable=True)
    fecha_actualizacion = Column(DateTime, server_default=func.now(), onupdate=func.now())
    
    hijo = relationship("Paciente", back_populates="historial")
    asistencias = relationship("AsistenciaMensual", back_populates="historial", cascade="all, delete-orphan")
    evoluciones = relationship("EvolucionObjetivo", back_populates="historial", cascade="all, delete-orphan")
    frecuencias = relationship("FrecuenciaTerapia", back_populates="historial", cascade="all, delete-orphan")

class AsistenciaMensual(Base):
    __tablename__ = "asistencias_mensuales"
    
    id = Column(Integer, primary_key=True, index=True)
    historial_id = Column(Integer, ForeignKey("historiales.id", ondelete="CASCADE"), nullable=False)
    mes = Column(String(20), nullable=False)
    asistidas = Column(Integer, default=0)
    canceladas = Column(Integer, default=0)
    
    historial = relationship("Historial", back_populates="asistencias")

class EvolucionObjetivo(Base):
    __tablename__ = "evoluciones_objetivos"
    
    id = Column(Integer, primary_key=True, index=True)
    historial_id = Column(Integer, ForeignKey("historiales.id", ondelete="CASCADE"), nullable=False)
    fecha = Column(Date, nullable=False)
    objetivo = Column(String(255), nullable=False)
    valor = Column(Integer, nullable=False)
    observaciones = Column(Text, nullable=True)
    
    historial = relationship("Historial", back_populates="evoluciones")

class FrecuenciaTerapia(Base):
    __tablename__ = "frecuencias_terapias"
    
    id = Column(Integer, primary_key=True, index=True)
    historial_id = Column(Integer, ForeignKey("historiales.id", ondelete="CASCADE"), nullable=False)
    tipo_terapia = Column(String(100), nullable=False)
    sesiones_por_semana = Column(Integer, default=1)
    total_sesiones = Column(Integer, default=0)
    
    historial = relationship("Historial", back_populates="frecuencias")