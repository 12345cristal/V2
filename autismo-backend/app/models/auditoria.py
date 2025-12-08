# app/models/auditoria.py
"""Modelo para Auditoría de acciones"""

from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.base_class import Base


class Auditoria(Base):
    __tablename__ = "auditoria"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"))
    modulo = Column(String(60))
    accion = Column(String(60))
    descripcion = Column(String)  # TEXT
    ip = Column(String(40))
    fecha = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    usuario = relationship("Usuario", back_populates="auditorias")
