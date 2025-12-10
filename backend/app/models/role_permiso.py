# app/models/role_permiso.py
from sqlalchemy import Column, Integer, ForeignKey, Table
from app.db.base_class import Base


class RolePermiso(Base):
    """Modelo de relación Roles-Permisos"""
    __tablename__ = "roles_permisos"
    
    rol_id = Column(Integer, ForeignKey("roles.id", ondelete="CASCADE", onupdate="CASCADE"), primary_key=True)
    permiso_id = Column(Integer, ForeignKey("permisos.id", ondelete="CASCADE", onupdate="CASCADE"), primary_key=True)
