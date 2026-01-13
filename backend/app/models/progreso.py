from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    ForeignKey,
    Float,
    Text
)
from sqlalchemy.orm import relationship
from datetime import datetime

from app.db.base_class import Base


class Progreso(Base):
    __tablename__ = "progresos"

    id = Column(Integer, primary_key=True, index=True)

    # FK CORRECTA → apunta a la tabla REAL: ninos
    nino_id = Column(
        Integer,
        ForeignKey("ninos.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    fecha = Column(DateTime, default=datetime.utcnow, nullable=False)

    area = Column(String(100), nullable=False)        # Ej: Lenguaje, Motricidad
    nivel = Column(String(50), nullable=True)         # Ej: Bajo, Medio, Alto
    puntuacion = Column(Float, nullable=True)         # Score numérico
    observaciones = Column(Text, nullable=True)

    # =========================
    # RELACIONES
    # =========================
    nino = relationship(
        "Nino",
        back_populates="progresos"
    )
