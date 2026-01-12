# app/models/recurso.py
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from .database import Base
from datetime import datetime

class Recurso(Base):
    __tablename__ = "recursos"
    
    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String(255), nullable=False)
    descripcion = Column(Text)
    tipo_recurso = Column(String(50), nullable=False)  # PDF, VIDEO, ENLACE
    categoria_recurso = Column(String(100))
    nivel_recurso = Column(String(50))
    url = Column(String(500))
    archivo = Column(String(500))
    objetivo_terapeutico = Column(Text)
    terapeuta_id = Column(Integer, ForeignKey("terapeutas.id"))
    fecha_creacion = Column(DateTime, default=datetime.now)
    
    terapeuta = relationship("Terapeuta", back_populates="recursos")
    recomendaciones = relationship("Recomendacion", back_populates="recurso")


class Recomendacion(Base):
    __tablename__ = "recomendaciones"
    
    id = Column(Integer, primary_key=True, index=True)
    recurso_id = Column(Integer, ForeignKey("recursos.id"))
    hijo_id = Column(Integer, ForeignKey("hijos.id"))
    terapeuta_id = Column(Integer, ForeignKey("terapeutas.id"))
    fecha_recomendacion = Column(DateTime, default=datetime.now)
    
    recurso = relationship("Recurso", back_populates="recomendaciones")
    hijo = relationship("Hijo")
    terapeuta = relationship("Terapeuta")


class RecursoVisto(Base):
    __tablename__ = "recursos_vistos"
    
    id = Column(Integer, primary_key=True, index=True)
    recurso_id = Column(Integer, ForeignKey("recursos.id"))
    usuario_id = Column(Integer, ForeignKey("usuarios.id"))
    fecha_visto = Column(DateTime, default=datetime.now)
    
    __table_args__ = (
        UniqueConstraint('recurso_id', 'usuario_id', name='uq_recurso_usuario'),
    )
