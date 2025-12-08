from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.db.session import Base

class Permiso(Base):
    __tablename__ = "permisos"

    id = Column(Integer, primary_key=True)
    codigo = Column(String(120), nullable=False, unique=True)
    descripcion = Column(String(150))

    roles_asignados = relationship("RolPermiso", back_populates="permiso")
