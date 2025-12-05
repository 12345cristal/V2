# app/models/permiso.py
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.db.session import Base


class Permiso(Base):
    __tablename__ = "permisos"

    id_permiso = Column(Integer, primary_key=True, index=True)
    codigo = Column(String(100), unique=True, nullable=False)  # ej. "PERSONAL_VER"
    nombre = Column(String(150), nullable=False)

    roles = relationship(
        "RolPermiso",
        back_populates="permiso",
        cascade="all, delete-orphan"
    )


class RolPermiso(Base):
    __tablename__ = "roles_permisos"

    id = Column(Integer, primary_key=True, index=True)
    id_rol = Column(Integer, nullable=False)
    id_permiso = Column(Integer, nullable=False)

    # relaciones
    rol = relationship("Rol", back_populates="permisos")
    permiso = relationship("Permiso", back_populates="roles")
