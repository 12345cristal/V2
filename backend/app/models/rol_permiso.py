# app/models/rol_permiso.py
from sqlalchemy import Column, Integer, ForeignKey, PrimaryKeyConstraint
from app.db.base_class import Base

class RolPermiso(Base):
    __tablename__ = "roles_permisos"

    rol_id = Column(Integer, ForeignKey("roles.id", ondelete="CASCADE", onupdate="CASCADE"), nullable=False)
    permiso_id = Column(Integer, ForeignKey("permisos.id", ondelete="CASCADE", onupdate="CASCADE"), nullable=False)

    __table_args__ = (
        PrimaryKeyConstraint("rol_id", "permiso_id"),
    )
