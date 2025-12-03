# app/models/decision_log.py
from datetime import datetime

from sqlalchemy import String, Text, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class DecisionLog(Base):
    __tablename__ = "decision_logs"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    tipo_decision: Mapped[str] = mapped_column(String(100), nullable=False)
    entrada_json: Mapped[str] = mapped_column(Text, nullable=False)
    resultado_json: Mapped[str] = mapped_column(Text, nullable=False)
    fecha: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, nullable=False
    )
    usuario_id: Mapped[int | None] = mapped_column(
        ForeignKey("usuarios.id", ondelete="SET NULL", onupdate="CASCADE"),
    )

    usuario = relationship("Usuario")
