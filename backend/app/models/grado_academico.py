# backend/app/models/grado_academico.py
from sqlalchemy import Column, Integer, String
from app.db.base_class import Base


class GradoAcademico(Base):
    """
    Catálogo de grados académicos
    """
    __tablename__ = "grado_academico"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(100), nullable=False, unique=True)
    descripcion = Column(String(255), nullable=True)
