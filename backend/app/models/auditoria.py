# app/models/auditoria.py
from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from app.db.base import Base


class Auditoria(Base):
    __tablename__ = "auditoria"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id", ondelete="SET NULL"))
    accion = Column(String(200))
    tabla_afectada = Column(String(100))
    registro_id = Column(Integer)
    fecha = Column(DateTime, default=datetime.utcnow)
