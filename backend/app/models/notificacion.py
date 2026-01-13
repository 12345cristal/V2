# app/models/notificacion.py
from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    ForeignKey,
    Text,
    SmallInteger
)
from sqlalchemy.orm import relationship
from datetime import datetime

from app.db.base_class import Base


class Notificacion(Base):
    __tablename__ = "notificaciones"

    id = Column(Integer, primary_key=True, index=True)

    usuario_id = Column(
        Integer,
        ForeignKey("usuarios.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    titulo = Column(String(200), nullable=False)
    mensaje = Column(Text, nullable=False)
    tipo = Column(String(50), nullable=False)  # TAREA, PAGO, CITA, GENERAL

    leida = Column(SmallInteger, default=0, nullable=False)
    fecha = Column(DateTime, default=datetime.utcnow, nullable=False)
    fecha_leida = Column(DateTime)

    metadata_json = Column(Text)

    # =========================
    # RELACIONES
    # =========================
    usuario = relationship(
        "Usuario",
        back_populates="notificaciones"
    )
