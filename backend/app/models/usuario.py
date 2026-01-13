from datetime import datetime

from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    DateTime,
    ForeignKey,
)
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class Usuario(Base):
    """
    Modelo principal de usuarios del sistema
    (autenticación, roles y relaciones base)
    """

    __tablename__ = "usuarios"

    # =========================
    # CAMPOS BASE
    # =========================
    id = Column(Integer, primary_key=True, index=True)

    nombres = Column(String(100), nullable=False)
    apellido_paterno = Column(String(60), nullable=False)
    apellido_materno = Column(String(60), nullable=True)

    email = Column(String(100), nullable=False, unique=True, index=True)
    hashed_password = Column(String(255), nullable=False)

    telefono = Column(String(20), nullable=True)

    activo = Column(Boolean, nullable=False, default=True)

    rol_id = Column(
        Integer,
        ForeignKey("roles.id", ondelete="RESTRICT"),
        nullable=False
    )

    fecha_creacion = Column(
        DateTime,
        nullable=False,
        default=datetime.utcnow
    )

    ultimo_login = Column(DateTime, nullable=True)

    # =========================
    # RELACIONES
    # =========================

    # 🔹 Rol del sistema
    rol = relationship(
        "Rol",
        back_populates="usuarios"
    )

    # 🔹 Perfil de personal (1 a 1)
    personal = relationship(
        "Personal",
        back_populates="usuario",
        uselist=False,
        cascade="all, delete-orphan"
    )

    # 🔹 Notificaciones del usuario
    notificaciones = relationship(
        "Notificacion",
        back_populates="usuario",
        cascade="all, delete-orphan"
    )

    # 🔹 Recursos vistos por el usuario
    recursos_vistos = relationship(
        "RecursoVisto",
        back_populates="usuario",
        cascade="all, delete-orphan"
    )

    # =========================
    # MÉTODOS ÚTILES
    # =========================
    @property
    def nombre_completo(self) -> str:
        return f"{self.nombres} {self.apellido_paterno} {self.apellido_materno or ''}".strip()

    def __repr__(self) -> str:
        return f"<Usuario id={self.id} email={self.email} activo={self.activo}>"
