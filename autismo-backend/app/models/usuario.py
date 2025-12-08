from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.session import Base

class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    nombres = Column(String(100), nullable=False)
    apellido_paterno = Column(String(60), nullable=False)
    apellido_materno = Column(String(60))
    email = Column(String(100), unique=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    rol_id = Column(Integer, ForeignKey("roles.id"), nullable=False)
    activo = Column(Boolean, default=True)
    ultimo_login = Column(DateTime)
    fecha_creacion = Column(DateTime, default=datetime.utcnow)

    # IMPORTACIÓN LOCAL para evitar circular import
    from app.models.rol import Rol
    rol = relationship("Rol", back_populates="usuarios")
