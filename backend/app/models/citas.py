# app/models/cita.py
from datetime import date, time

from sqlalchemy import (
    String, Text, Boolean, Date, Time, ForeignKey, Integer
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class Cita(Base):
    __tablename__ = "citas"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    # Niño existente (puede ser NULL si es nuevo)
    nino_id: Mapped[int | None] = mapped_column(
        ForeignKey("ninos.id", ondelete="SET NULL", onupdate="CASCADE")
    )

    # Bandera para indicar si es nuevo niño
    es_nuevo_nino: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    # Datos temporales para nuevo niño
    temp_nino_nombre: Mapped[str | None] = mapped_column(String(100))
    temp_nino_apellido_paterno: Mapped[str | None] = mapped_column(String(50))
    temp_nino_apellido_materno: Mapped[str | None] = mapped_column(String(50))
    temp_tutor_nombre: Mapped[str | None] = mapped_column(String(100))
    temp_tutor_apellido_paterno: Mapped[str | None] = mapped_column(String(50))
    temp_tutor_apellido_materno: Mapped[str | None] = mapped_column(String(50))
    telefono_temporal: Mapped[str | None] = mapped_column(String(20))

    terapeuta_id: Mapped[int | None] = mapped_column(
        ForeignKey("personal.id", ondelete="SET NULL", onupdate="CASCADE")
    )
    terapia_id: Mapped[int | None] = mapped_column(
        ForeignKey("terapias.id", ondelete="SET NULL", onupdate="CASCADE")
    )

    fecha: Mapped[date] = mapped_column(Date, nullable=False)
    hora_inicio: Mapped[time] = mapped_column(Time, nullable=False)
    hora_fin: Mapped[time] = mapped_column(Time, nullable=False)

    estado_id: Mapped[int] = mapped_column(
        ForeignKey("cat_estado_cita.id", ondelete="RESTRICT", onupdate="CASCADE"),
        nullable=False,
    )

    es_reposicion: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    motivo: Mapped[str | None] = mapped_column(Text)
    diagnostico_presuntivo: Mapped[str | None] = mapped_column(String(255))
    observaciones: Mapped[str | None] = mapped_column(Text)

    # Relaciones
    nino = relationship("Nino")
    terapeuta = relationship("Personal")
    terapia = relationship("Terapia")
    estado = relationship("CatEstadoCita")
    observadores = relationship("CitaObservador", back_populates="cita")


class CitaObservador(Base):
    __tablename__ = "citas_observadores"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    cita_id: Mapped[int] = mapped_column(
        ForeignKey("citas.id", ondelete="CASCADE", onupdate="CASCADE")
    )
    terapeuta_id: Mapped[int] = mapped_column(
        ForeignKey("personal.id", ondelete="CASCADE", onupdate="CASCADE")
    )

    cita = relationship("Cita", back_populates="observadores")
    terapeuta = relationship("Personal")
