# app/models/nino.py
from sqlalchemy import (
    Column, Integer, String, Date, Enum, DateTime, Text,
    Boolean, ForeignKey
)
from sqlalchemy.orm import relationship
from app.db.base_class import Base


class Nino(Base):
    __tablename__ = "ninos"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    apellido_paterno = Column(String(50), nullable=False)
    apellido_materno = Column(String(50))
    fecha_nacimiento = Column(Date, nullable=False)
    sexo = Column(Enum("M", "F", "O"), nullable=False)
    curp = Column(String(18))
    tutor_principal_id = Column(Integer, ForeignKey("tutores.id", ondelete="SET NULL"))
    fecha_registro = Column(DateTime)
    estado = Column(Enum("ACTIVO", "BAJA_TEMPORAL", "INACTIVO"), nullable=False, default="ACTIVO")

    # Relaciones 1-1
    direccion = relationship("NinoDireccion", uselist=False, back_populates="nino")
    diagnostico = relationship("NinoDiagnostico", uselist=False, back_populates="nino")
    escolar = relationship("NinoEscolar", uselist=False, back_populates="nino")
    info_emocional = relationship("NinoInfoEmocional", uselist=False, back_populates="nino")
    archivos = relationship("NinoArchivos", uselist=False, back_populates="nino")
    alergias = relationship("NinoAlergias", uselist=False, back_populates="nino")

    # Relaciones 1-N
    medicamentos_actuales = relationship("NinoMedicamentoActual", back_populates="nino")
    contactos_emergencia = relationship("NinoContactoEmergencia", back_populates="nino")


class NinoDireccion(Base):
    __tablename__ = "ninos_direccion"

    id = Column(Integer, primary_key=True)
    nino_id = Column(Integer, ForeignKey("ninos.id", ondelete="CASCADE"), nullable=False)
    calle = Column(String(200))
    numero = Column(String(20))
    colonia = Column(String(200))
    municipio = Column(String(100))
    codigo_postal = Column(String(10))

    nino = relationship("Nino", back_populates="direccion")


class NinoDiagnostico(Base):
    __tablename__ = "ninos_diagnostico"

    id = Column(Integer, primary_key=True)
    nino_id = Column(Integer, ForeignKey("ninos.id", ondelete="CASCADE"), nullable=False)
    diagnostico_principal = Column(String(255), nullable=False)
    diagnostico_resumen = Column(String(255))
    diagnostico_url = Column(String(255))
    fecha_diagnostico = Column(Date)
    especialista = Column(String(200))
    institucion = Column(String(200))

    nino = relationship("Nino", back_populates="diagnostico")


class NinoAlergias(Base):
    __tablename__ = "ninos_alergias"

    id = Column(Integer, primary_key=True)
    nino_id = Column(Integer, ForeignKey("ninos.id", ondelete="CASCADE"), nullable=False)
    medicamentos = Column(Text)
    alimentos = Column(Text)
    ambiental = Column(Text)

    nino = relationship("Nino", back_populates="alergias")


class NinoMedicamentoActual(Base):
    __tablename__ = "ninos_medicamentos_actuales"

    id = Column(Integer, primary_key=True)
    nino_id = Column(Integer, ForeignKey("ninos.id", ondelete="CASCADE"), nullable=False)
    sin_medicamentos = Column(Boolean, default=False)
    nombre = Column(String(200))
    dosis = Column(String(100))
    horario = Column(String(100))

    nino = relationship("Nino", back_populates="medicamentos_actuales")


class NinoEscolar(Base):
    __tablename__ = "ninos_escolar"

    id = Column(Integer, primary_key=True)
    nino_id = Column(Integer, ForeignKey("ninos.id", ondelete="CASCADE"), nullable=False)
    asiste_escuela = Column(Boolean, default=True)
    escuela = Column(String(255))
    grado = Column(String(100))
    director_nombre = Column(String(200))
    director_telefono = Column(String(20))
    horario_clases = Column(String(100))
    adaptaciones = Column(Text)

    nino = relationship("Nino", back_populates="escolar")


class NinoContactoEmergencia(Base):
    __tablename__ = "ninos_contactos_emergencia"

    id = Column(Integer, primary_key=True)
    nino_id = Column(Integer, ForeignKey("ninos.id", ondelete="CASCADE"), nullable=False)
    nombre_completo = Column(String(200))
    relacion = Column(String(100))
    telefono = Column(String(20))
    telefono_secundario = Column(String(20))
    direccion = Column(Text)

    nino = relationship("Nino", back_populates="contactos_emergencia")


class NinoInfoEmocional(Base):
    __tablename__ = "ninos_info_emocional"

    id = Column(Integer, primary_key=True)
    nino_id = Column(Integer, ForeignKey("ninos.id", ondelete="CASCADE"), nullable=False)
    estimulos_ansiedad = Column(Text)
    cosas_que_calman = Column(Text)
    preferencias_sensoriales = Column(Text)
    cosas_no_tolera = Column(Text)
    palabras_clave = Column(Text)
    forma_comunicacion = Column(String(200))
    nivel_comprension = Column(
        Enum("ALTO", "MEDIO", "BAJO"),
        nullable=False,
        default="MEDIO"
    )

    nino = relationship("Nino", back_populates="info_emocional")


class NinoArchivos(Base):
    __tablename__ = "ninos_archivos"

    id = Column(Integer, primary_key=True)
    nino_id = Column(Integer, ForeignKey("ninos.id", ondelete="CASCADE"), nullable=False)
    acta_nacimiento_url = Column(String(255))
    curp_url = Column(String(255))
    comprobante_domicilio_url = Column(String(255))
    foto_url = Column(String(255))
    diagnostico_url = Column(String(255))
    consentimiento_url = Column(String(255))
    hoja_ingreso_url = Column(String(255))

    nino = relationship("Nino", back_populates="archivos")
