# app/models/terapia.py
"""Modelos para Terapias, Sesiones y Reposiciones"""

from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, SmallInteger, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.base_class import Base


class Terapia(Base):
    __tablename__ = "terapias"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(100), nullable=False)
    descripcion = Column(String)  # TEXT
    tipo_id = Column(SmallInteger, ForeignKey("tipo_terapia.id"), nullable=False)
    duracion_minutos = Column(Integer, nullable=False)
    objetivo_general = Column(String)  # TEXT
    activo = Column(SmallInteger, default=1)
    
    # Relationships
    tipo = relationship("TipoTerapia", back_populates="terapias")
    personal_asignado = relationship("TerapiaPersonal", back_populates="terapia")
    asignaciones_ninos = relationship("TerapiaNino", back_populates="terapia")
    citas = relationship("Cita", back_populates="terapia")
    reposiciones = relationship("Reposicion", back_populates="terapia")


class TerapiaPersonal(Base):
    __tablename__ = "terapias_personal"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    terapia_id = Column(Integer, ForeignKey("terapias.id", ondelete="CASCADE"), nullable=False)
    personal_id = Column(Integer, ForeignKey("personal.id", ondelete="CASCADE"), nullable=False)
    activo = Column(SmallInteger, default=1)
    
    # Relationships
    terapia = relationship("Terapia", back_populates="personal_asignado")
    personal = relationship("Personal", back_populates="terapias_asignadas")


class TerapiaNino(Base):
    __tablename__ = "terapias_nino"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    nino_id = Column(Integer, ForeignKey("ninos.id", ondelete="CASCADE"), nullable=False)
    terapia_id = Column(Integer, ForeignKey("terapias.id", ondelete="CASCADE"), nullable=False)
    terapeuta_id = Column(Integer, ForeignKey("personal.id", ondelete="SET NULL"))
    prioridad_id = Column(SmallInteger, ForeignKey("prioridad.id"), nullable=False)
    frecuencia_semana = Column(Integer, nullable=False)
    fecha_asignacion = Column(DateTime, default=datetime.utcnow)
    activo = Column(SmallInteger, default=1)
    
    # Relationships
    nino = relationship("Nino", back_populates="terapias")
    terapia = relationship("Terapia", back_populates="asignaciones_ninos")
    terapeuta = relationship("Personal", back_populates="terapias_nino")
    prioridad = relationship("Prioridad", back_populates="terapias_nino")
    sesiones = relationship("Sesion", back_populates="terapia_nino")


class Sesion(Base):
    __tablename__ = "sesiones"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    terapia_nino_id = Column(Integer, ForeignKey("terapias_nino.id", ondelete="CASCADE"), nullable=False)
    fecha = Column(DateTime, nullable=False)
    asistio = Column(SmallInteger, default=1)
    progreso = Column(Integer)  # 0-100
    colaboracion = Column(Integer)  # 0-100
    observaciones = Column(String)  # TEXT
    creado_por = Column(Integer, ForeignKey("personal.id", ondelete="SET NULL"))
    
    # Relationships
    terapia_nino = relationship("TerapiaNino", back_populates="sesiones")
    creado_por_personal = relationship("Personal", back_populates="sesiones_creadas")


class Reposicion(Base):
    __tablename__ = "reposiciones"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    nino_id = Column(Integer, ForeignKey("ninos.id"), nullable=False)
    terapia_id = Column(Integer, ForeignKey("terapias.id"), nullable=False)
    fecha_original = Column(DateTime, nullable=False)
    fecha_nueva = Column(DateTime, nullable=False)
    motivo = Column(String)  # TEXT
    estado = Column(Enum('PENDIENTE', 'APROBADA', 'RECHAZADA'), default='PENDIENTE')
    
    # Relationships
    nino = relationship("Nino", back_populates="reposiciones")
    terapia = relationship("Terapia", back_populates="reposiciones")
