# app/models/catalogos.py
from sqlalchemy import Column, Integer, String
from app.db.base import Base


class CatGradoAcademico(Base):
    __tablename__ = "cat_grado_academico"

    id = Column(Integer, primary_key=True, autoincrement=True)
    codigo = Column(String(30), nullable=False, unique=True)
    nombre = Column(String(80), nullable=False)


class CatEstadoLaboral(Base):
    __tablename__ = "cat_estado_laboral"

    id = Column(Integer, primary_key=True, autoincrement=True)
    codigo = Column(String(30), nullable=False, unique=True)
    nombre = Column(String(80), nullable=False)


class CatTipoTerapia(Base):
    __tablename__ = "cat_tipo_terapia"

    id = Column(Integer, primary_key=True, autoincrement=True)
    codigo = Column(String(30), nullable=False, unique=True)
    nombre = Column(String(80), nullable=False)


class CatPrioridad(Base):
    __tablename__ = "cat_prioridad"

    id = Column(Integer, primary_key=True, autoincrement=True)
    codigo = Column(String(20), nullable=False, unique=True)
    nombre = Column(String(80), nullable=False)


class CatEstadoCita(Base):
    __tablename__ = "cat_estado_cita"

    id = Column(Integer, primary_key=True, autoincrement=True)
    codigo = Column(String(30), nullable=False, unique=True)
    nombre = Column(String(80), nullable=False)


class CatNivelDificultad(Base):
    __tablename__ = "cat_nivel_dificultad"

    id = Column(Integer, primary_key=True, autoincrement=True)
    codigo = Column(String(20), nullable=False, unique=True)
    nombre = Column(String(80), nullable=False)


class CatTipoRecurso(Base):
    __tablename__ = "cat_tipo_recurso"

    id = Column(Integer, primary_key=True, autoincrement=True)
    codigo = Column(String(30), nullable=False, unique=True)
    nombre = Column(String(80), nullable=False)


class CatCategoriaRecurso(Base):
    __tablename__ = "cat_categoria_recurso"

    id = Column(Integer, primary_key=True, autoincrement=True)
    codigo = Column(String(30), nullable=False, unique=True)
    nombre = Column(String(80), nullable=False)


class CatNivelRecurso(Base):
    __tablename__ = "cat_nivel_recurso"

    id = Column(Integer, primary_key=True, autoincrement=True)
    codigo = Column(String(30), nullable=False, unique=True)
    nombre = Column(String(80), nullable=False)
