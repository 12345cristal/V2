# app/models/rol.py
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String
from app.db.session import Base

class Rol(Base):
    __tablename__ = "roles"
    id = Column(Integer, primary_key=True)
    nombre = Column(String)
    descripcion = Column(String)

    permisos = relationship("RolPermiso", back_populates="rol")
    usuarios = relationship("Usuario", back_populates="rol")
