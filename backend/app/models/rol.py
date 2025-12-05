# app/models/rol.py
from sqlalchemy import Boolean, Column, Integer, String
from app.db.base import Base


class Rol(Base):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nombre = Column(String(50), nullable=False, unique=True)
    descripcion = Column(String(70))
    activo = Column(Boolean, nullable=False, default=True)
