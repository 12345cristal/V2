# app/models/auditoria.py
from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.db.base import Base


class Auditoria(Base):
    __tablename__ = "auditoria"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    usuario_id = Column(
        Integer,
        ForeignKey("usuarios.id", ondelete="SET NULL", onupdate="CASCADE"),
    )
    accion = Column(String(200))
    tabla_afectada = Column(String(100))
    registro_id = Column(Integer)
    fecha = Column(DateTime, default=datetime.utcnow)

    usuario = relationship("Usuario")
