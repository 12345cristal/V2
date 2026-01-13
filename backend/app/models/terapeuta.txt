from sqlalchemy import (
    Column, Integer, String, Text, Date, DateTime,
    Boolean, Float, ForeignKey
)
from sqlalchemy.orm import relationship
from datetime import datetime

from app.db.base_class import Base


class Padre(Base):
    __tablename__ = "padres"

    id = Column(Integer, primary_key=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), unique=True)
    telefono = Column(String(20))
    direccion = Column(String(500))
    ocupacion = Column(String(255))

    usuario = relationship("Usuario", back_populates="padre")
    hijos = relationship("Hijo", back_populates="padre")


class Terapeuta(Base):
    __tablename__ = "terapeutas"

    id = Column(Integer, primary_key=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), unique=True)
    especialidad = Column(String(255))
    cedula_profesional = Column(String(100))
    telefono = Column(String(20))
    anos_experiencia = Column(Integer)
    biografia = Column(Text)

    usuario = relationship("Usuario", back_populates="terapeuta")
    recursos = relationship("Recurso", back_populates="terapeuta")
    sesiones = relationship("Sesion", back_populates="terapeuta")


class Hijo(Base):
    __tablename__ = "hijos"

    id = Column(Integer, primary_key=True)
    nombre = Column(String(255), nullable=False)
    apellido = Column(String(255), nullable=False)
    fecha_nacimiento = Column(Date, nullable=False)
    diagnostico = Column(String(255))
    nivel_tea = Column(String(50))
    observaciones = Column(Text)
    foto_perfil = Column(String(500))

    padre_id = Column(Integer, ForeignKey("padres.id"))

    padre = relationship("Padre", back_populates="hijos")
    sesiones = relationship("Sesion", back_populates="hijo")
    progresos = relationship("Progreso", back_populates="hijo")


class Progreso(Base):
    __tablename__ = "progresos"

    id = Column(Integer, primary_key=True)
    hijo_id = Column(Integer, ForeignKey("hijos.id"))
    fecha = Column(DateTime, default=datetime.utcnow)
    area = Column(String(100))
    nivel = Column(String(50))
    puntuacion = Column(Float)
    observaciones = Column(Text)

    hijo = relationship("Hijo", back_populates="progresos")
