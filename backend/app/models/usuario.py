# app/models/usuario.py
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base_class import Base

class Usuario(Base):
  __tablename__ = "usuarios"

  id = Column(Integer, primary_key=True, index=True)
  nombres = Column(String(100), nullable=False)
  apellido_paterno = Column(String(50), nullable=False)
  apellido_materno = Column(String(50))
  email = Column(String(80), unique=True, nullable=False, index=True)
  hashed_password = Column(String(255), nullable=False)
  rol_id = Column(Integer, ForeignKey("roles.id"), nullable=False)
  telefono = Column(String(20))
  activo = Column(Boolean, default=True)
  fecha_creacion = Column(DateTime)
  ultimo_login = Column(DateTime)

  rol = relationship("Rol", back_populates="usuarios")
