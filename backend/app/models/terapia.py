# app/models/terapia.py
from sqlalchemy import Column, Integer, String, Text, ForeignKey, DECIMAL, SmallInteger
from sqlalchemy.orm import relationship
from app.db.base_class import Base


class Terapia(Base):
    """
    Modelo para la tabla 'terapias'
    Representa las diferentes terapias que se ofrecen en el centro
    """
    __tablename__ = "terapias"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nombre = Column(String(100), nullable=False)
    descripcion = Column(Text)
    tipo_id = Column(SmallInteger, ForeignKey("tipo_terapia.id"), nullable=False)
    duracion_minutos = Column(Integer, nullable=False, default=60)
    objetivo_general = Column(Text)
    activo = Column(SmallInteger, default=1)

    # Relaciones
    tipo_terapia = relationship("TipoTerapia", back_populates="terapias")
    personal_asignado = relationship("TerapiaPersonal", back_populates="terapia", cascade="all, delete-orphan")
    terapias_nino = relationship("TerapiaNino", back_populates="terapia", cascade="all, delete-orphan")


class TerapiaPersonal(Base):
    """
    Modelo para la tabla 'terapias_personal'
    Asignación de personal (terapeutas) a terapias
    """
    __tablename__ = "terapias_personal"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    terapia_id = Column(Integer, ForeignKey("terapias.id", ondelete="CASCADE"), nullable=False)
    personal_id = Column(Integer, ForeignKey("personal.id", ondelete="CASCADE"), nullable=False)
    activo = Column(SmallInteger, default=1)

    # Relaciones
    terapia = relationship("Terapia", back_populates="personal_asignado")
    personal = relationship("Personal", back_populates="terapias_asignadas")


class TerapiaNino(Base):
    """
    Modelo para la tabla 'terapias_nino'
    Asignación de terapias a niños con su terapeuta y prioridad
    """
    __tablename__ = "terapias_nino"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nino_id = Column(Integer, ForeignKey("ninos.id", ondelete="CASCADE"), nullable=False)
    terapia_id = Column(Integer, ForeignKey("terapias.id", ondelete="CASCADE"), nullable=False)
    terapeuta_id = Column(Integer, ForeignKey("personal.id", ondelete="SET NULL"))
    prioridad_id = Column(SmallInteger, ForeignKey("prioridad.id"), nullable=False)
    frecuencia_semana = Column(Integer, nullable=False)
    fecha_asignacion = Column(String(50), nullable=True)
    activo = Column(SmallInteger, default=1)

    # Relaciones
    nino = relationship("Nino", back_populates="terapias")
    terapia = relationship("Terapia", back_populates="terapias_nino")
    terapeuta = relationship("Personal", foreign_keys=[terapeuta_id])
    prioridad = relationship("Prioridad")
    sesiones = relationship("Sesion", back_populates="terapia_nino", cascade="all, delete-orphan")


class TipoTerapia(Base):
    """
    Catálogo de tipos de terapia
    """
    __tablename__ = "tipo_terapia"

    id = Column(SmallInteger, primary_key=True, autoincrement=True)
    codigo = Column(String(30), nullable=False, unique=True)
    nombre = Column(String(80), nullable=False)

    # Relaciones
    terapias = relationship("Terapia", back_populates="tipo_terapia")


class Prioridad(Base):
    """
    Catálogo de prioridades para terapias
    """
    __tablename__ = "prioridad"

    id = Column(SmallInteger, primary_key=True, autoincrement=True)
    codigo = Column(String(20), nullable=False, unique=True)
    nombre = Column(String(80), nullable=False)


class Sesion(Base):
    """
    Modelo para la tabla 'sesiones'
    Registra las sesiones de terapia realizadas
    """
    __tablename__ = "sesiones"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    terapia_nino_id = Column(Integer, ForeignKey("terapias_nino.id", ondelete="CASCADE"), nullable=False)
    fecha = Column(String(50), nullable=False)
    asistio = Column(SmallInteger, default=1)
    progreso = Column(Integer)
    colaboracion = Column(Integer)
    observaciones = Column(Text)
    creado_por = Column(Integer, ForeignKey("personal.id", ondelete="SET NULL"))

    # Relaciones
    terapia_nino = relationship("TerapiaNino", back_populates="sesiones")
    creador = relationship("Personal", foreign_keys=[creado_por])


class Reposicion(Base):
    """
    Modelo para la tabla 'reposiciones'
    Gestión de reposiciones de sesiones
    """
    __tablename__ = "reposiciones"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nino_id = Column(Integer, ForeignKey("ninos.id"), nullable=False)
    terapia_id = Column(Integer, ForeignKey("terapias.id"), nullable=False)
    fecha_original = Column(String(50), nullable=False)
    fecha_nueva = Column(String(50), nullable=False)
    motivo = Column(Text)
    estado = Column(String(20), default='PENDIENTE')  # PENDIENTE, APROBADA, RECHAZADA

    # Relaciones
    nino = relationship("Nino")
    terapia = relationship("Terapia")
