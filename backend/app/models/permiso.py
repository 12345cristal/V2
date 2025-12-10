# app/models/permiso.py
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.db.base_class import Base


class Permiso(Base):
    """Modelo de Permisos"""
    __tablename__ = "permisos"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    codigo = Column(String(120), nullable=False, unique=True)
    descripcion = Column(String(150))
    
    # Relaciones
    roles = relationship("Rol", secondary="roles_permisos", back_populates="permisos")
