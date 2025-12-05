# app/models/usuario.py
from sqlalchemy import Column, Integer, String, ForeignKey, Enum, Boolean, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime

from app.db.session import Base


class EstadoUsuarioEnum(str, Enum):
    ACTIVO = "ACTIVO"
    INACTIVO = "INACTIVO"
    BLOQUEADO = "BLOQUEADO"


class Usuario(Base):
    __tablename__ = "usuarios"

    id_usuario = Column(Integer, primary_key=True, index=True)
    id_personal = Column(Integer, ForeignKey("personal.id_personal"), nullable=False)
    username = Column(String(100), unique=True, nullable=False)
    email = Column(String(150), unique=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    rol_sistema = Column(String(50), nullable=False)
    estado = Column(Enum(EstadoUsuarioEnum), default=EstadoUsuarioEnum.ACTIVO)
    debe_cambiar_password = Column(Boolean, default=False)
    fecha_creacion = Column(DateTime, default=datetime.utcnow)
    ultima_sesion = Column(DateTime, nullable=True)

    personal = relationship("Personal", back_populates="usuario")
    rol = relationship("Rol")  # si enlazas rol_sistema -> roles.nombre_rol
