# app/models/notificacion.py
"""Modelo para Notificaciones"""

from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, SmallInteger
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.base_class import Base


class Notificacion(Base):
    __tablename__ = "notificaciones"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    titulo = Column(String(200))
    mensaje = Column(String)  # TEXT
    tipo = Column(String(40))
    leida = Column(SmallInteger, default=0)
    fecha = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    usuario = relationship("Usuario", back_populates="notificaciones")
