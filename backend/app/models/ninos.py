from sqlalchemy import (
    Column,
    Integer,
    String,
    Date,
    DateTime,
    Enum as SAEnum,
    Text,
    Boolean,
    ForeignKey,
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.base import Base


class Nino(Base):
    __tablename__ = "ninos"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(100), nullable=False)
    apellido_paterno = Column(String(50), nullable=False)
    apellido_materno = Column(String(50))
    fecha_nacimiento = Column(Date, nullable=False)
    sexo = Column(SAEnum("M", "F", "O", name="sexo_enum"), nullable=False)
    curp = Column(String(18))
    tutor_principal_id = Column(Integer, ForeignKey("tutores.id", ondelete="SET NULL", onupdate="CASCADE"))
    fecha_registro = Column(DateTime, nullable=False, server_default=func.current_timestamp())
    estado = Column(SAEnum("ACTIVO", "BAJA_TEMPORAL", "INACTIVO", name="estado_nino_enum"), nullable=False, default="ACTIVO")

    tutor_principal = relationship("Tutor", back_populates="ninos_principales")
    direccion = relationship("NinoDireccion", back_populates="nino", uselist=False)
    diagnostico = relationship("NinoDiagnostico", back_populates="nino", uselist=False)
    alergias = relationship("NinoAlergias", back_populates="nino", uselist=False)
    medicamentos_actuales = relationship("NinoMedicamentoActual", back_populates="nino")
    escolar = relationship("NinoEscolar", back_populates="nino", uselist=False)
    contactos_emergencia = relationship("NinoContactoEmergencia", back_populates="nino")
    info_emocional = relationship("NinoInfoEmocional", back_populates="nino", uselist=False)
    archivos = relationship("NinoArchivos", back_populates="nino")
    terapias_nino = relationship("TerapiaNino", back_populates="nino")
    citas = relationship("Cita", back_populates="nino")
    recursos_tareas = relationship("RecursoTarea", back_populates="nino")
    recomendaciones_actividades = relationship("RecomendacionActividad", back_populates="nino")


class NinoDireccion(Base):
    __tablename__ = "ninos_direccion"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nino_id = Column(Integer, ForeignKey("ninos.id", ondelete="CASCADE"), nullable=False)
    calle = Column(String(200))
    numero = Column(String(20))
    colonia = Column(String(200))
    municipio = Column(String(100))
    codigo_postal = Column(String(10))

    nino = relationship("Nino", back_populates="direccion")


class NinoDiagnostico(Base):
    __tablename__ = "ninos_diagnostico"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nino_id = Column(Integer, ForeignKey("ninos.id", ondelete="CASCADE"), nullable=False, unique=True)
    diagnostico_principal = Column(String(255), nullable=False)
    diagnostico_resumen = Column(String(255))
    diagnostico_url = Column(String(255))
    fecha_diagnostico = Column(Date)
    especialista = Column(String(200))
    institucion = Column(String(200))

    nino = relationship("Nino", back_populates="diagnostico")


class NinoAlergias(Base):
    __tablename__ = "ninos_alergias"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nino_id = Column(Integer, ForeignKey("ninos.id", ondelete="CASCADE"), nullable=False)
    medicamentos = Column(Text)
    alimentos = Column(Text)
    ambiental = Column(Text)

    nino = relationship("Nino", back_populates="alergias")


class NinoMedicamentoActual(Base):
    __tablename__ = "ninos_medicamentos_actuales"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nino_id = Column(Integer, ForeignKey("ninos.id", ondelete="CASCADE"), nullable=False)
    sin_medicamentos = Column(Boolean, nullable=False, default=False)
    nombre = Column(String(200))
    dosis = Column(String(100))
    horario = Column(String(100))

    nino = relationship("Nino", back_populates="medicamentos_actuales")


class NinoEscolar(Base):
    __tablename__ = "ninos_escolar"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nino_id = Column(Integer, ForeignKey("ninos.id", ondelete="CASCADE"), nullable=False, unique=True)
    asiste_escuela = Column(Boolean, nullable=False, default=True)
    escuela = Column(String(255))
    grado = Column(String(100))
    director_nombre = Column(String(200))
    director_telefono = Column(String(20))
    horario_clases = Column(String(100))
    adaptaciones = Column(Text)

    nino = relationship("Nino", back_populates="escolar")


class NinoContactoEmergencia(Base):
    __tablename__ = "ninos_contactos_emergencia"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nino_id = Column(Integer, ForeignKey("ninos.id", ondelete="CASCADE"), nullable=False)
    nombre_completo = Column(String(200))
    relacion = Column(String(100))
    telefono = Column(String(20))
    telefono_secundario = Column(String(20))
    direccion = Column(Text)

    nino = relationship("Nino", back_populates="contactos_emergencia")


class NinoInfoEmocional(Base):
    __tablename__ = "ninos_info_emocional"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nino_id = Column(Integer, ForeignKey("ninos.id", ondelete="CASCADE"), nullable=False, unique=True)
    estimulos_ansiedad = Column(Text)
    cosas_que_calman = Column(Text)
    preferencias_sensoriales = Column(Text)
    cosas_no_tolera = Column(Text)
    palabras_clave = Column(Text)
    forma_comunicacion = Column(String(200))
    nivel_comprension = Column(
        SAEnum("ALTO", "MEDIO", "BAJO", name="nivel_comprension_enum"),
        nullable=False,
        default="MEDIO",
    )

    nino = relationship("Nino", back_populates="info_emocional")


class NinoArchivos(Base):
    __tablename__ = "ninos_archivos"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nino_id = Column(Integer, ForeignKey("ninos.id", ondelete="CASCADE"), nullable=False)
    acta_nacimiento_url = Column(String(255))
    curp_url = Column(String(255))
    comprobante_domicilio_url = Column(String(255))
    foto_url = Column(String(255))
    diagnostico_url = Column(String(255))
    consentimiento_url = Column(String(255))
    hoja_ingreso_url = Column(String(255))

    nino = relationship("Nino", back_populates="archivos")
