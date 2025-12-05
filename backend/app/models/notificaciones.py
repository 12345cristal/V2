from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    Boolean,
    DateTime,
    ForeignKey,
    Enum as SAEnum,
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.base import Base


class Notificacion(Base):
    __tablename__ = "notificaciones"

    id = Column(Integer, primary_key=True, autoincrement=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id", ondelete="CASCADE"), nullable=False)
    titulo = Column(String(200))
    mensaje = Column(Text)
    tipo = Column(SAEnum("cambio-horario", "reposicion", "documento", "alerta", name="tipo_notificacion_enum"))
    leida = Column(Boolean, default=False)
    fecha_creacion = Column(DateTime, server_default=func.current_timestamp())

    usuario = relationship("Usuario", back_populates="notificaciones")
