# app/models/nino.py
from datetime import datetime
from sqlalchemy import Column, Integer, String, Date, Enum, DateTime, ForeignKey, Text, JSON
from sqlalchemy.orm import relationship
from app.db.base_class import Base


class Nino(Base):
    """Modelo de Niños beneficiarios"""
    __tablename__ = "ninos"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    apellido_paterno = Column(String(60), nullable=False)
    apellido_materno = Column(String(60))
    fecha_nacimiento = Column(Date, nullable=False)
    sexo = Column(Enum("M", "F", "O", name="sexo_enum"), nullable=False)
    curp = Column(String(18))
    tutor_id = Column(Integer, ForeignKey("tutores.id"))
    estado = Column(
        Enum("ACTIVO", "INACTIVO", name="estado_nino_enum"),
        default="ACTIVO"
    )
    fecha_registro = Column(DateTime, default=datetime.utcnow)
    
    # Campo para recomendación basada en contenido
    # Almacena perfil vectorizado: tags, diagnóstico, dificultades, intereses
    perfil_contenido = Column(JSON, default=dict)

    # Relaciones
    tutor = relationship("Tutor", back_populates="ninos")
    direccion = relationship("NinoDireccion", back_populates="nino", uselist=False, cascade="all, delete-orphan")
    diagnostico = relationship("NinoDiagnostico", back_populates="nino", uselist=False, cascade="all, delete-orphan")
    info_emocional = relationship("NinoInfoEmocional", back_populates="nino", uselist=False, cascade="all, delete-orphan")
    archivos = relationship("NinoArchivos", back_populates="nino", uselist=False, cascade="all, delete-orphan")
    terapias = relationship("TerapiaNino", back_populates="nino", cascade="all, delete-orphan")
    medicamentos = relationship("Medicamento", back_populates="nino", cascade="all, delete-orphan")
    alergias = relationship("Alergia", back_populates="nino", cascade="all, delete-orphan")


class NinoDireccion(Base):
    """Dirección del niño"""
    __tablename__ = "ninos_direccion"

    id = Column(Integer, primary_key=True, index=True)
    nino_id = Column(Integer, ForeignKey("ninos.id", ondelete="CASCADE"), unique=True, nullable=False)
    calle = Column(String(200))
    numero = Column(String(20))
    colonia = Column(String(200))
    municipio = Column(String(100))
    codigo_postal = Column(String(10))

    nino = relationship("Nino", back_populates="direccion")


class NinoDiagnostico(Base):
    """Diagnóstico del niño"""
    __tablename__ = "ninos_diagnostico"

    id = Column(Integer, primary_key=True, index=True)
    nino_id = Column(Integer, ForeignKey("ninos.id", ondelete="CASCADE"), unique=True, nullable=False)
    diagnostico_principal = Column(String(255))
    diagnostico_resumen = Column(String(255))
    archivo_url = Column(String(255))
    fecha_diagnostico = Column(Date)
    especialista = Column(String(200))
    institucion = Column(String(200))

    nino = relationship("Nino", back_populates="diagnostico")


class NinoInfoEmocional(Base):
    """Información emocional y de comportamiento del niño"""
    __tablename__ = "ninos_info_emocional"

    id = Column(Integer, primary_key=True, index=True)
    nino_id = Column(Integer, ForeignKey("ninos.id", ondelete="CASCADE"), unique=True, nullable=False)
    estimulos = Column(Text)
    calmantes = Column(Text)
    preferencias = Column(Text)
    no_tolera = Column(Text)
    palabras_clave = Column(Text)
    forma_comunicacion = Column(String(200))
    nivel_comprension = Column(
        Enum("ALTO", "MEDIO", "BAJO", name="nivel_comprension_enum"),
        default="MEDIO"
    )

    nino = relationship("Nino", back_populates="info_emocional")


class NinoArchivos(Base):
    """Archivos del niño"""
    __tablename__ = "ninos_archivos"

    id = Column(Integer, primary_key=True, index=True)
    nino_id = Column(Integer, ForeignKey("ninos.id", ondelete="CASCADE"), unique=True, nullable=False)
    acta_url = Column(String(255))
    curp_url = Column(String(255))
    comprobante_url = Column(String(255))
    foto_url = Column(String(255))
    diagnostico_url = Column(String(255))
    consentimiento_url = Column(String(255))
    hoja_ingreso_url = Column(String(255))

    nino = relationship("Nino", back_populates="archivos")
