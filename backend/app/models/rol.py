# app/models/rol.py
from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship
from app.db.base_class import Base


class Rol(Base):
    """Modelo de Roles"""
    __tablename__ = "roles"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(50), nullable=False, unique=True)
    descripcion = Column(String(100))
    activo = Column(Boolean, nullable=False, default=True)
    
    # Relaciones
    usuarios = relationship("Usuario", back_populates="rol")
    personal = relationship("Personal", back_populates="rol")
    permisos = relationship("Permiso", secondary="roles_permisos", back_populates="roles")
