# app/models/actividad.py
from sqlalchemy import Column, Integer, String, Text, JSON, DECIMAL, SmallInteger
from app.db.base_class import Base


class Actividad(Base):
    """
    Modelo para actividades terapéuticas
    Representa actividades que se pueden recomendar para cada niño
    """
    __tablename__ = "actividades"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nombre = Column(String(150), nullable=False)
    descripcion = Column(Text)
    objetivo = Column(Text)
    materiales = Column(Text)
    duracion_minutos = Column(Integer, default=30)
    
    # Campos para recomendación basada en contenido
    tags = Column(JSON, default=list)  # Lista de palabras clave: ['motricidad', 'lenguaje', 'social']
    dificultad = Column(SmallInteger, default=1)  # 1=Bajo, 2=Medio, 3=Alto
    area_desarrollo = Column(String(100))  # 'cognitivo', 'motor', 'lenguaje', 'social', 'emocional'
    
    activo = Column(SmallInteger, default=1)

    def __repr__(self):
        return f"<Actividad(id={self.id}, nombre='{self.nombre}', dificultad={self.dificultad})>"
