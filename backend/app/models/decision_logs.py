# app/models/decision_logs.py
from datetime import datetime

from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    DateTime,
    ForeignKey,
)
from sqlalchemy.orm import relationship

from app.db.base import Base


class DecisionLog(Base):
    __tablename__ = "decision_logs"

    id = Column(Integer, primary_key=True, autoincrement=True)
    tipo_decision = Column(String(100), nullable=False)
    entrada_json = Column(Text, nullable=False)
    resultado_json = Column(Text, nullable=False)
    fecha = Column(DateTime, default=datetime.utcnow)
    usuario_id = Column(
        Integer,
        ForeignKey("usuarios.id", ondelete="SET NULL", onupdate="CASCADE"),
    )

    usuario = relationship("Usuario")
