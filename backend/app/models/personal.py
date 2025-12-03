# app/models/personal.py
from sqlalchemy import String, Integer, Enum, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class Personal(Base):
    __tablename__ = "personal"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    usuario_id: Mapped[int] = mapped_column(
        ForeignKey("usuarios.id", ondelete="CASCADE", onupdate="CASCADE"),
        unique=True,
    )
    rol_id: Mapped[int] = mapped_column(
        ForeignKey("roles.id", ondelete="RESTRICT", onupdate="CASCADE"),
        nullable=False,
    )
    cedula_profesional: Mapped[str | None] = mapped_column(String(20))
    cedula_estatus: Mapped[str] = mapped_column(
        Enum("VALIDA", "EN_TRAMITE", "NO_APLICA", name="cedula_estatus_enum"),
        default="NO_APLICA",
        nullable=False,
    )
    especialidad: Mapped[str | None] = mapped_column(String(100))
    anio_experiencia: Mapped[int] = mapped_column(Integer, default=0)

    usuario = relationship("Usuario", back_populates="personal")
    rol = relationship("Rol")
