from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.db.base_class import Base


class Permiso(Base):
    __tablename__ = "permisos"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    codigo = Column(String(120), nullable=False, unique=True)
    descripcion = Column(String(150))
    
    # Relationships
    roles_asignados = relationship("RolePermiso", back_populates="permiso")
