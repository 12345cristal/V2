# app/models/nino.py
from datetime import datetime, date

from sqlalchemy import String, Enum, Date, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class Nino(Base):
    __tablename__ = "ninos"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    nombre: Mapped[str] = mapped_column(String(100), nullable=False)
    apellido_paterno: Mapped[str] = mapped_column(String(50), nullable=False)
    apellido_materno: Mapped[str | None] = mapped_column(String(50))
    fecha_nacimiento: Mapped[date] = mapped_column(Date, nullable=False)
    sexo: Mapped[str] = mapped_column(
        Enum("M", "F", "O", name="sexo_enum"),
        nullable=False,
    )
    curp: Mapped[str | None] = mapped_column(String(18))
    tutor_principal_id: Mapped[int | None] = mapped_column(
        ForeignKey("tutores.id", ondelete="SET NULL", onupdate="CASCADE"),
    )
    fecha_registro: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=datetime.utcnow
    )
    estado: Mapped[str] = mapped_column(
        Enum("ACTIVO", "BAJA_TEMPORAL", "INACTIVO", name="estado_nino_enum"),
        default="ACTIVO",
        nullable=False,
    )

    tutor_principal = relationship("Tutor", back_populates="ninos")
