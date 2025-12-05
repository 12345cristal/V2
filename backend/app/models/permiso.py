# app/models/permiso.py
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.db.base_class import Base

class Permiso(Base):
    __tablename__ = "permisos"

    id = Column(Integer, primary_key=True, index=True)
    codigo = Column(String(100), unique=True, nullable=False)
    descripcion = Column(String(100))

    roles = relationship(
        "Rol",
        secondary="roles_permisos",
        back_populates="permisos"
    )
