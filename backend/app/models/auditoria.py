from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    ForeignKey,
)
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.db.base import Base


class Auditoria(Base):
    __tablename__ = "auditoria"

    id = Column(Integer, primary_key=True, autoincrement=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id", ondelete="SET NULL"))
    accion = Column(String(200))
    tabla_afectada = Column(String(100))
    registro_id = Column(Integer)
    fecha = Column(DateTime, server_default=func.current_timestamp())

    usuario = relationship("Usuario")
