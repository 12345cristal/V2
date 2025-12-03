# app/models/catalogos.py
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class CatGradoAcademico(Base):
    __tablename__ = "cat_grado_academico"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    codigo: Mapped[str] = mapped_column(String(30), unique=True, nullable=False)
    nombre: Mapped[str] = mapped_column(String(80), nullable=False)


class CatEstadoLaboral(Base):
    __tablename__ = "cat_estado_laboral"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    codigo: Mapped[str] = mapped_column(String(30), unique=True, nullable=False)
    nombre: Mapped[str] = mapped_column(String(80), nullable=False)


class CatTipoTerapia(Base):
    __tablename__ = "cat_tipo_terapia"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    codigo: Mapped[str] = mapped_column(String(30), unique=True, nullable=False)
    nombre: Mapped[str] = mapped_column(String(80), nullable=False)


class CatPrioridad(Base):
    __tablename__ = "cat_prioridad"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    codigo: Mapped[str] = mapped_column(String(20), unique=True, nullable=False)
    nombre: Mapped[str] = mapped_column(String(80), nullable=False)


class CatEstadoCita(Base):
    __tablename__ = "cat_estado_cita"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    codigo: Mapped[str] = mapped_column(String(30), unique=True, nullable=False)
    nombre: Mapped[str] = mapped_column(String(80), nullable=False)


class CatNivelDificultad(Base):
    __tablename__ = "cat_nivel_dificultad"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    codigo: Mapped[str] = mapped_column(String(20), unique=True, nullable=False)
    nombre: Mapped[str] = mapped_column(String(80), nullable=False)


class CatTipoRecurso(Base):
    __tablename__ = "cat_tipo_recurso"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    codigo: Mapped[str] = mapped_column(String(30), unique=True, nullable=False)
    nombre: Mapped[str] = mapped_column(String(80), nullable=False)


class CatCategoriaRecurso(Base):
    __tablename__ = "cat_categoria_recurso"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    codigo: Mapped[str] = mapped_column(String(30), unique=True, nullable=False)
    nombre: Mapped[str] = mapped_column(String(80), nullable=False)


class CatNivelRecurso(Base):
    __tablename__ = "cat_nivel_recurso"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    codigo: Mapped[str] = mapped_column(String(30), unique=True, nullable=False)
    nombre: Mapped[str] = mapped_column(String(80), nullable=False)
