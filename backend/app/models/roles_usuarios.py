from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    DateTime,
    ForeignKey,
    Text,
    SmallInteger,
    Enum as SAEnum,
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db.base import Base


class Rol(Base):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(50), nullable=False, unique=True)
    descripcion = Column(String(70))
    activo = Column(Boolean, nullable=False, default=True)

    usuarios = relationship("Usuario", back_populates="rol")
    permisos = relationship(
        "Permiso",
        secondary="roles_permisos",
        back_populates="roles",
        lazy="joined",
    )


class Permiso(Base):
    __tablename__ = "permisos"

    id = Column(Integer, primary_key=True, autoincrement=True)
    codigo = Column(String(100), nullable=False, unique=True)
    descripcion = Column(String(100))

    roles = relationship(
        "Rol",
        secondary="roles_permisos",
        back_populates="permisos",
    )


class RolPermiso(Base):
    __tablename__ = "roles_permisos"

    rol_id = Column(Integer, ForeignKey("roles.id", ondelete="CASCADE", onupdate="CASCADE"), primary_key=True)
    permiso_id = Column(Integer, ForeignKey("permisos.id", ondelete="CASCADE", onupdate="CASCADE"), primary_key=True)


class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nombres = Column(String(100), nullable=False)
    apellido_paterno = Column(String(50), nullable=False)
    apellido_materno = Column(String(50))
    email = Column(String(80), nullable=False, unique=True)
    hashed_password = Column(String(255), nullable=False)
    rol_id = Column(Integer, ForeignKey("roles.id", ondelete="RESTRICT", onupdate="CASCADE"), nullable=False)
    telefono = Column(String(20))
    activo = Column(Boolean, nullable=False, default=True)
    fecha_creacion = Column(DateTime, nullable=False, server_default=func.current_timestamp())
    ultimo_login = Column(DateTime)

    rol = relationship("Rol", back_populates="usuarios")
    perfil_personal = relationship("PerfilPersonal", back_populates="usuario", uselist=False)
    personal = relationship("Personal", back_populates="usuario", uselist=False)
    tutor = relationship("Tutor", back_populates="usuario", uselist=False)
    notificaciones = relationship("Notificacion", back_populates="usuario")


class PerfilPersonal(Base):
    __tablename__ = "perfiles_personal"

    id = Column(Integer, primary_key=True, autoincrement=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id", ondelete="CASCADE", onupdate="CASCADE"), nullable=False, unique=True)
    fecha_nacimiento = Column(DateTime, nullable=False)
    grado_academico_id = Column(SmallInteger, ForeignKey("cat_grado_academico.id", ondelete="SET NULL", onupdate="CASCADE"))
    especialidad_principal = Column(String(100))
    especialidades = Column(Text)
    rfc = Column(String(13))
    ine_numero = Column(String(18))
    ine_url = Column(String(255))
    curp = Column(String(18))
    telefono_personal = Column(String(15))
    correo_personal = Column(String(50))
    domicilio_calle = Column(String(70))
    domicilio_colonia = Column(String(70))
    domicilio_cp = Column(String(10))
    domicilio_municipio = Column(String(70))
    domicilio_estado = Column(String(70))
    cv_url = Column(String(255))
    experiencia = Column(String(200))
    fecha_ingreso = Column(DateTime)
    estado_laboral_id = Column(SmallInteger, ForeignKey("cat_estado_laboral.id", ondelete="SET NULL", onupdate="CASCADE"))
    total_pacientes = Column(Integer, default=0)
    sesiones_semana = Column(Integer, default=0)
    rating = Column(SAEnum("0.00", name="rating_placeholder"), nullable=True)  # puedes ajustar a DECIMAL en servicios

    usuario = relationship("Usuario", back_populates="perfil_personal")
    # relaciones hacia catálogos se pueden usar si quieres: grado_academico, estado_laboral


class Personal(Base):
    __tablename__ = "personal"

    id = Column(Integer, primary_key=True, autoincrement=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id", ondelete="CASCADE", onupdate="CASCADE"), nullable=False, unique=True)
    rol_id = Column(Integer, ForeignKey("roles.id", ondelete="RESTRICT", onupdate="CASCADE"), nullable=False)
    cedula_profesional = Column(String(20))
    cedula_estatus = Column(SAEnum("VALIDA", "EN_TRAMITE", "NO_APLICA", name="cedula_estatus_enum"), nullable=False, default="NO_APLICA")
    especialidad = Column(String(100))
    anio_experiencia = Column(Integer, default=0)

    usuario = relationship("Usuario", back_populates="personal")
    rol = relationship("Rol")
    terapias = relationship("PersonalTerapia", back_populates="personal")
    terapias_nino = relationship("TerapiaNino", back_populates="terapeuta")
    sesiones_creadas = relationship("SesionTerapia", back_populates="creado_por")
    recursos = relationship("RecursoTerapeuta", back_populates="personal")
    citas = relationship("Cita", back_populates="terapeuta")
