# app/models/auditoria.py

from sqlalchemy import Column, Integer, String, DateTime, JSON, Text
from datetime import datetime

from app.db.base_class import Base


class Auditoria(Base):
    __tablename__ = "auditoria"

    id_auditoria = Column(Integer, primary_key=True, index=True)
    fecha_hora = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Información del usuario que realiza la acción
    usuario_id = Column(Integer, nullable=True)  # puede ser None si el token es inválido
    usuario_nombre = Column(String(150), nullable=True)
    rol_usuario = Column(String(100), nullable=True)

    # Información de la acción
    modulo = Column(String(100), nullable=False)
    accion = Column(String(50), nullable=False)
    detalle = Column(JSON, nullable=True)  # se puede usar JSON para registrar payloads
    descripcion = Column(Text, nullable=True)  # descripción textual opcional

    # Información adicional
    ip = Column(String(50), nullable=True)
