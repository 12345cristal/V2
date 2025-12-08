# app/models/rol.py
from sqlalchemy import Column, Integer, String, SmallInteger
from sqlalchemy.orm import relationship
from app.db.base_class import Base


class Rol(Base):
    __tablename__ = "roles"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(50), nullable=False, unique=True)
    descripcion = Column(String(100))
    activo = Column(SmallInteger, nullable=False, default=1)
    
    # Relationships
    usuarios = relationship("Usuario", back_populates="rol")
    permisos = relationship("RolePermiso", back_populates="rol")
