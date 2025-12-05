# app/models/permiso.py
from sqlalchemy import Column, Integer, String
from app.db.base import Base


class Permiso(Base):
    __tablename__ = "permisos"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    codigo = Column(String(100), nullable=False, unique=True)
    descripcion = Column(String(100))
