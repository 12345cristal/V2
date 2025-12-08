# app/models/catalogos.py
"""Modelos para tablas de catálogos/lookups"""

from sqlalchemy import Column, Integer, String, SmallInteger
from sqlalchemy.orm import relationship
from app.db.base_class import Base


class GradoAcademico(Base):
    __tablename__ = "grado_academico"
    
    id = Column(SmallInteger, primary_key=True, autoincrement=True)
    codigo = Column(String(30), nullable=False, unique=True)
    nombre = Column(String(80), nullable=False)
    
    # Relationships
    personal_perfiles = relationship("PersonalPerfil", back_populates="grado_academico")


class EstadoLaboral(Base):
    __tablename__ = "estado_laboral"
    
    id = Column(SmallInteger, primary_key=True, autoincrement=True)
    codigo = Column(String(30), nullable=False, unique=True)
    nombre = Column(String(80), nullable=False)
    
    # Relationships
    personal = relationship("Personal", back_populates="estado_laboral")


class TipoTerapia(Base):
    __tablename__ = "tipo_terapia"
    
    id = Column(SmallInteger, primary_key=True, autoincrement=True)
    codigo = Column(String(30), nullable=False, unique=True)
    nombre = Column(String(80), nullable=False)
    
    # Relationships
    terapias = relationship("Terapia", back_populates="tipo")


class Prioridad(Base):
    __tablename__ = "prioridad"
    
    id = Column(SmallInteger, primary_key=True, autoincrement=True)
    codigo = Column(String(20), nullable=False, unique=True)
    nombre = Column(String(80), nullable=False)
    
    # Relationships
    terapias_nino = relationship("TerapiaNino", back_populates="prioridad")


class EstadoCita(Base):
    __tablename__ = "estado_cita"
    
    id = Column(SmallInteger, primary_key=True, autoincrement=True)
    codigo = Column(String(30), nullable=False, unique=True)
    nombre = Column(String(80), nullable=False)
    
    # Relationships
    citas = relationship("Cita", back_populates="estado")


class NivelDificultad(Base):
    __tablename__ = "nivel_dificultad"
    
    id = Column(SmallInteger, primary_key=True, autoincrement=True)
    codigo = Column(String(20), nullable=False, unique=True)
    nombre = Column(String(80), nullable=False)


class TipoRecurso(Base):
    __tablename__ = "tipo_recurso"
    
    id = Column(SmallInteger, primary_key=True, autoincrement=True)
    codigo = Column(String(30), nullable=False, unique=True)
    nombre = Column(String(80), nullable=False)
    
    # Relationships
    recursos = relationship("Recurso", back_populates="tipo")


class CategoriaRecurso(Base):
    __tablename__ = "categoria_recurso"
    
    id = Column(SmallInteger, primary_key=True, autoincrement=True)
    codigo = Column(String(30), nullable=False, unique=True)
    nombre = Column(String(80), nullable=False)
    
    # Relationships
    recursos = relationship("Recurso", back_populates="categoria")


class NivelRecurso(Base):
    __tablename__ = "nivel_recurso"
    
    id = Column(SmallInteger, primary_key=True, autoincrement=True)
    codigo = Column(String(30), nullable=False, unique=True)
    nombre = Column(String(80), nullable=False)
    
    # Relationships
    recursos = relationship("Recurso", back_populates="nivel")
