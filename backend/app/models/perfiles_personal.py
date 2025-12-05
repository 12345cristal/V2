# app/models/perfiles_personal.py
from sqlalchemy import (
    Column,
    Integer,
    String,
    Date,
    Text,
    ForeignKey,
    SmallInteger,
    Numeric,
)
from sqlalchemy.orm import relationship

from app.db.base import Base


class PerfilPersonal(Base):
    __tablename__ = "perfiles_personal"

    id = Column(Integer, primary_key=True, autoincrement=True)
    usuario_id = Column(
        Integer,
        ForeignKey("usuarios.id", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False,
        unique=True,
    )
    fecha_nacimiento = Column(Date, nullable=False)
    grado_academico_id = Column(
        SmallInteger,
        ForeignKey("cat_grado_academico.id", ondelete="SET NULL", onupdate="CASCADE"),
        nullable=True,
    )
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
    fecha_ingreso = Column(Date)
    estado_laboral_id = Column(
        SmallInteger,
        ForeignKey("cat_estado_laboral.id", ondelete="SET NULL", onupdate="CASCADE"),
        nullable=True,
    )
    total_pacientes = Column(Integer, default=0)
    sesiones_semana = Column(Integer, default=0)
    rating = Column(Numeric(3, 2))

    usuario = relationship("Usuario", back_populates="perfil_personal", lazy="joined")
    grado_academico = relationship("CatGradoAcademico", lazy="joined")
    estado_laboral = relationship("CatEstadoLaboral", lazy="joined")
