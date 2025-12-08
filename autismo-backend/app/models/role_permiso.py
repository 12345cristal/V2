from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base_class import Base


class RolePermiso(Base):
    __tablename__ = "roles_permisos"
    
    rol_id = Column(Integer, ForeignKey("roles.id", ondelete="CASCADE", onupdate="CASCADE"), primary_key=True)
    permiso_id = Column(Integer, ForeignKey("permisos.id", ondelete="CASCADE", onupdate="CASCADE"), primary_key=True)
    
    # Relationships
    rol = relationship("Rol", back_populates="permisos")
    permiso = relationship("Permiso", back_populates="roles_asignados")
