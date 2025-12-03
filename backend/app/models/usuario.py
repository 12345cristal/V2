# app/models/usuario.py
from datetime import datetime

from sqlalchemy import String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class Usuario(Base):
    __tablename__ = "usuarios"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    nombres: Mapped[str] = mapped_column(String(100), nullable=False)
    apellido_paterno: Mapped[str] = mapped_column(String(50), nullable=False)
    apellido_materno: Mapped[str | None] = mapped_column(String(50))
    email: Mapped[str] = mapped_column(String(80), unique=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    rol_id: Mapped[int] = mapped_column(ForeignKey("roles.id"), nullable=False)
    telefono: Mapped[str | None] = mapped_column(String(20))
    activo: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    fecha_creacion: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, nullable=False
    )
    ultimo_login: Mapped[datetime | None] = mapped_column(DateTime)

    rol = relationship("Rol", back_populates="usuarios")

    # Relaciones a futuro
    perfil_personal = relationship(
        "PerfilPersonal",
        back_populates="usuario",
        uselist=False,
    )
    personal = relationship(
        "Personal",
        back_populates="usuario",
        uselist=False,
    )
    tutor = relationship(
        "Tutor",
        back_populates="usuario",
        uselist=False,
    )
    notificaciones = relationship(
        "Notificacion",
        back_populates="usuario",
        cascade="all, delete-orphan",
    )
