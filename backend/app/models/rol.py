# app/models/rol.py
from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship
from app.db.base_class import Base

class Rol(Base):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(50), unique=True, nullable=False)
    descripcion = Column(String(70))
    activo = Column(Boolean, default=True)

    usuarios = relationship("Usuario", back_populates="rol")
    permisos = relationship(
        "Permiso",
        secondary="roles_permisos",
        back_populates="roles"
    )
