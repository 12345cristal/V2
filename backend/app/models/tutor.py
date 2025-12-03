# app/models/tutor.py
from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class Tutor(Base):
    __tablename__ = "tutores"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    usuario_id: Mapped[int] = mapped_column(
        ForeignKey("usuarios.id", ondelete="CASCADE", onupdate="CASCADE"),
        unique=True,
    )
    ocupacion: Mapped[str | None] = mapped_column(String(100))
    notas: Mapped[str | None] = mapped_column()

    usuario = relationship("Usuario", back_populates="tutor")
    ninos = relationship("Nino", back_populates="tutor_principal")
