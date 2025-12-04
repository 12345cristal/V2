# app/models/perfil_personal.py
from sqlalchemy import Date, String, ForeignKey, Text, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class PerfilPersonal(Base):
    __tablename__ = "perfiles_personal"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    usuario_id: Mapped[int] = mapped_column(
        ForeignKey("usuarios.id", ondelete="CASCADE", onupdate="CASCADE"),
        unique=True
    )

    fecha_nacimiento: Mapped[Date]
    grado_academico_id: Mapped[int | None]
    especialidad_principal: Mapped[str | None] = mapped_column(String(100))
    especialidades: Mapped[str | None] = mapped_column(Text)

    rfc: Mapped[str | None] = mapped_column(String(13))
    ine_numero: Mapped[str | None] = mapped_column(String(18))
    ine_url: Mapped[str | None] = mapped_column(String(255))

    curp: Mapped[str | None] = mapped_column(String(18))
    telefono_personal: Mapped[str | None] = mapped_column(String(15))
    correo_personal: Mapped[str | None] = mapped_column(String(50))

    domicilio_calle: Mapped[str | None] = mapped_column(String(70))
    domicilio_colonia: Mapped[str | None] = mapped_column(String(70))
    domicilio_cp: Mapped[str | None] = mapped_column(String(10))
    domicilio_municipio: Mapped[str | None] = mapped_column(String(70))
    domicilio_estado: Mapped[str | None] = mapped_column(String(70))

    cv_url: Mapped[str | None] = mapped_column(String(255))
    experiencia: Mapped[str | None] = mapped_column(String(200))
    fecha_ingreso: Mapped[Date | None]

    estado_laboral_id: Mapped[int | None]
    total_pacientes: Mapped[int] = mapped_column(default=0)
    sesiones_semana: Mapped[int] = mapped_column(default=0)
    rating: Mapped[float | None]

    personal = relationship("Personal", back_populates="perfil")
