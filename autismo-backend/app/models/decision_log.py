# app/models/decision_log.py
"""Modelo para logs de decisiones IA y TOPSIS"""

from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.base_class import Base


class DecisionLog(Base):
    __tablename__ = "decision_logs"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    tipo = Column(String(60))  # 'TOPSIS', 'GEMINI_RESUMEN', 'GEMINI_SUGERENCIAS', etc.
    entrada_json = Column(String)  # TEXT - JSON con los parámetros de entrada
    salida_json = Column(String)  # TEXT - JSON con el resultado
    usuario_id = Column(Integer, ForeignKey("usuarios.id"))
    fecha = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    usuario = relationship("Usuario", back_populates="decision_logs")
