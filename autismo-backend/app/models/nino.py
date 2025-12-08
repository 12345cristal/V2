# app/models/nino.py
"""Modelos para Niños beneficiados"""

from sqlalchemy import Column, Integer, String, ForeignKey, Date, Enum, DateTime, SmallInteger
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.base_class import Base


class Nino(Base):
    __tablename__ = "ninos"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(100), nullable=False)
    apellido_paterno = Column(String(60), nullable=False)
    apellido_materno = Column(String(60))
    fecha_nacimiento = Column(Date, nullable=False)
    sexo = Column(Enum('M', 'F', 'O'), nullable=False)
    curp = Column(String(18))
    tutor_id = Column(Integer, ForeignKey("tutores.id", ondelete="SET NULL"))
    estado = Column(Enum('ACTIVO', 'BAJA_TEMPORAL', 'INACTIVO'), default='ACTIVO')
    fecha_registro = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    tutor = relationship("Tutor", back_populates="ninos")
    direccion = relationship("NinoDireccion", back_populates="nino", uselist=False)
    diagnostico = relationship("NinoDiagnostico", back_populates="nino", uselist=False)
    info_emocional = relationship("NinoInfoEmocional", back_populates="nino", uselist=False)
    archivos = relationship("NinoArchivos", back_populates="nino", uselist=False)
    terapias = relationship("TerapiaNino", back_populates="nino")
    citas = relationship("Cita", back_populates="nino")
    tareas = relationship("TareaRecurso", back_populates="nino")
    recomendaciones = relationship("Recomendacion", back_populates="nino")
    reposiciones = relationship("Reposicion", back_populates="nino")


class NinoDireccion(Base):
    __tablename__ = "ninos_direccion"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    nino_id = Column(Integer, ForeignKey("ninos.id", ondelete="CASCADE"), nullable=False, unique=True)
    calle = Column(String(200))
    numero = Column(String(20))
    colonia = Column(String(200))
    municipio = Column(String(100))
    codigo_postal = Column(String(10))
    
    # Relationships
    nino = relationship("Nino", back_populates="direccion")


class NinoDiagnostico(Base):
    __tablename__ = "ninos_diagnostico"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    nino_id = Column(Integer, ForeignKey("ninos.id", ondelete="CASCADE"), nullable=False, unique=True)
    diagnostico_principal = Column(String(255))
    diagnostico_resumen = Column(String(255))
    archivo_url = Column(String(255))
    fecha_diagnostico = Column(Date)
    especialista = Column(String(200))
    institucion = Column(String(200))
    
    # Relationships
    nino = relationship("Nino", back_populates="diagnostico")


class NinoInfoEmocional(Base):
    __tablename__ = "ninos_info_emocional"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    nino_id = Column(Integer, ForeignKey("ninos.id", ondelete="CASCADE"), nullable=False, unique=True)
    estimulos = Column(String)  # TEXT
    calmantes = Column(String)  # TEXT
    preferencias = Column(String)  # TEXT
    no_tolera = Column(String)  # TEXT
    palabras_clave = Column(String)  # TEXT
    forma_comunicacion = Column(String(200))
    nivel_comprension = Column(Enum('ALTO', 'MEDIO', 'BAJO'), default='MEDIO')
    
    # Relationships
    nino = relationship("Nino", back_populates="info_emocional")


class NinoArchivos(Base):
    __tablename__ = "ninos_archivos"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    nino_id = Column(Integer, ForeignKey("ninos.id", ondelete="CASCADE"), nullable=False, unique=True)
    acta_url = Column(String(255))
    curp_url = Column(String(255))
    comprobante_url = Column(String(255))
    foto_url = Column(String(255))
    diagnostico_url = Column(String(255))
    consentimiento_url = Column(String(255))
    hoja_ingreso_url = Column(String(255))
    
    # Relationships
    nino = relationship("Nino", back_populates="archivos")
