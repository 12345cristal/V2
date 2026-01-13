from datetime import datetime
from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    DateTime,
    ForeignKey,
    UniqueConstraint,
)
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class Recurso(Base):
    """Recursos terapéuticos creados por personal"""

    __tablename__ = "recursos"

    id = Column(Integer, primary_key=True, index=True)

    titulo = Column(String(255), nullable=False)
    descripcion = Column(Text)

    tipo_recurso = Column(String(50), nullable=False)  # PDF, VIDEO, ENLACE
    categoria_recurso = Column(String(100))
    nivel_recurso = Column(String(50))

    url = Column(String(500))
    archivo = Column(String(500))
    objetivo_terapeutico = Column(Text)

    terapeuta_id = Column(Integer, ForeignKey("personal.id"), nullable=False)

    fecha_creacion = Column(DateTime, default=datetime.utcnow)

    # =========================
    # Relaciones
    # =========================
    terapeuta = relationship("Personal", back_populates="recursos")

    recomendaciones = relationship(
        "Recomendacion",
        back_populates="recurso",
        cascade="all, delete-orphan",
    )

    vistos = relationship(
        "RecursoVisto",
        back_populates="recurso",
        cascade="all, delete-orphan",
    )
