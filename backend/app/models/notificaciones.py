# app/models/notificaciones.py
from datetime import datetime

from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    DateTime,
    Boolean,
    Enum,
    ForeignKey,
)
from sqlalchemy.orm import relationship

from app.db.base import Base


NOTIF_TIPO_ENUM = ("cambio-horario", "reposicion", "documento", "alerta")


class Notificacion(Base):
    __tablename__ = "notificaciones"

    id = Column(Integer, primary_key=True, autoincrement=True)
    usuario_id = Column(
        Integer,
        ForeignKey("usuarios.id", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False,
    )
    titulo = Column(String(200))
    mensaje = Column(Text)
    tipo = Column(Enum(*NOTIF_TIPO_ENUM, name="notificacion_tipo_enum"))
    leida = Column(Boolean, default=False)
    fecha_creacion = Column(DateTime, default=datetime.utcnow)

    usuario = relationship("Usuario")
