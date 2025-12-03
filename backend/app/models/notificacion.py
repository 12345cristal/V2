# app/models/notificacion.py
from datetime import datetime

from sqlalchemy import String, Text, Boolean, DateTime, ForeignKey, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class Notificacion(Base):
    __tablename__ = "notificaciones"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    usuario_id: Mapped[int] = mapped_column(
        ForeignKey("usuarios.id", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False,
    )
    titulo: Mapped[str | None] = mapped_column(String(200))
    mensaje: Mapped[str | None] = mapped_column(Text)
    tipo: Mapped[str] = mapped_column(
        Enum("cambio-horario", "reposicion", "documento", "alerta",
             name="tipo_notificacion_enum"),
        default="alerta",
        nullable=False,
    )
    leida: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    fecha_creacion: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, nullable=False
    )

    usuario = relationship("Usuario", back_populates="notificaciones")
