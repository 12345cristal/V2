# app/models/usuario.py
from datetime import datetime

from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
)
from sqlalchemy.orm import relationship

from app.db.base import Base
from app.models.rol import Rol


class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nombres = Column(String(100), nullable=False)
    apellido_paterno = Column(String(50), nullable=False)
    apellido_materno = Column(String(50))
    email = Column(String(80), nullable=False, unique=True, index=True)
    hashed_password = Column(String(255), nullable=False)
    rol_id = Column(Integer, ForeignKey("roles.id", ondelete="RESTRICT", onupdate="CASCADE"), nullable=False)
    telefono = Column(String(20))
    activo = Column(Boolean, nullable=False, default=True)
    fecha_creacion = Column(DateTime, nullable=False, default=datetime.utcnow)
    ultimo_login = Column(DateTime)

    rol = relationship("Rol", lazy="joined")
