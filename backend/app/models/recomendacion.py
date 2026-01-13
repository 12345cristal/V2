# app/models/recomendacion.py
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, JSON, Float
from sqlalchemy.orm import relationship
from app.db.base_class import Base


class PerfilNinoVectorizado(Base):
    """
    Almacena el perfil vectorizado del niño para recomendaciones
    Generado por Gemini a partir de notas clínicas, diagnósticos, historial
    """
    __tablename__ = "perfil_nino_vectorizado"

    id = Column(Integer, primary_key=True, index=True)
    nino_id = Column(Integer, ForeignKey("ninos.id", ondelete="CASCADE"), unique=True, nullable=False)
    
    # Vector de embeddings generado por Gemini
    embedding = Column(JSON, nullable=False)  # Array de floats
    
    # Metadatos para contexto
    edad = Column(Integer)
    diagnosticos = Column(JSON)  # ['TEA', 'TDAH', 'Retraso lenguaje']
    dificultades = Column(JSON)  # ['sensibilidad auditiva', 'hiperfoco visual']
    fortalezas = Column(JSON)  # ['memoria visual', 'reconocimiento patrones']
    
    # Texto original usado para generar embedding
    texto_perfil = Column(Text)
    
    # Control de actualizaciones
    fecha_generacion = Column(DateTime, default=datetime.utcnow)
    fecha_actualizacion = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relación
    nino = relationship("Nino", backref="perfil_vectorizado")


class PerfilActividadVectorizada(Base):
    """
    Almacena el perfil vectorizado de cada actividad
    """
    __tablename__ = "perfil_actividad_vectorizada"

    id = Column(Integer, primary_key=True, index=True)
    actividad_id = Column(Integer, ForeignKey("actividades.id", ondelete="CASCADE"), unique=True, nullable=False)
    
    # Vector de embeddings generado por Gemini
    embedding = Column(JSON, nullable=False)
    
    # Metadatos
    areas_desarrollo = Column(JSON)  # ['cognitivo', 'motor']
    tags = Column(JSON)  # ['lenguaje', 'imitación', 'visual']
    nivel_dificultad = Column(Integer)  # 1-3
    
    # Texto original
    texto_descripcion = Column(Text)
    
    fecha_generacion = Column(DateTime, default=datetime.utcnow)
    fecha_actualizacion = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relación
    actividad = relationship("Actividad", backref="perfil_vectorizado")


class HistorialProgreso(Base):
    """
    Registra el progreso del niño en actividades para aprendizaje colaborativo
    """
    __tablename__ = "historial_progreso"

    id = Column(Integer, primary_key=True, index=True)
    nino_id = Column(Integer, ForeignKey("ninos.id", ondelete="CASCADE"), nullable=False)
    actividad_id = Column(Integer, ForeignKey("actividades.id"), nullable=False)
    terapeuta_id = Column(Integer, ForeignKey("personal.id"), nullable=False)
    
    # Evaluación del progreso
    calificacion = Column(Float)  # 1.0 - 5.0
    notas_progreso = Column(Text)
    
    # Contexto
    fecha_sesion = Column(DateTime, nullable=False)
    duracion_minutos = Column(Integer)
    
    # Embedding de notas para análisis de similitud
    embedding_notas = Column(JSON)
    
    fecha_registro = Column(DateTime, default=datetime.utcnow)
    
    # Relaciones
    nino = relationship("Nino", backref="historial_progreso")
    actividad = relationship("Actividad", backref="historial_uso")
    terapeuta = relationship("Personal", backref="sesiones_registradas")


class RecomendacionActividad(Base):
    """
    Almacena recomendaciones generadas por el sistema
    """
    __tablename__ = "recomendaciones_actividades"

    id = Column(Integer, primary_key=True, index=True)
    nino_id = Column(Integer, ForeignKey("ninos.id", ondelete="CASCADE"), nullable=False)
    
    # Actividades recomendadas (ordenadas por score)
    actividades_recomendadas = Column(JSON, nullable=False)  # [{"actividad_id": 1, "score": 0.95, "razon": "..."}]
    
    # Explicación generada por Gemini
    explicacion_humana = Column(Text)
    
    # Método usado
    metodo = Column(String(50), default="contenido")  # 'contenido', 'colaborativo', 'hibrido'
    
    # Metadata
    fecha_generacion = Column(DateTime, default=datetime.utcnow)
    aplicada = Column(Integer, default=0)  # 0=No, 1=Sí
    
    # Relación
    nino = relationship("Nino", backref="recomendaciones_actividades")


class AsignacionTerapeutaTOPSIS(Base):
    """
    Almacena resultados de selección de terapeuta usando TOPSIS
    """
    __tablename__ = "asignaciones_terapeuta_topsis"

    id = Column(Integer, primary_key=True, index=True)
    nino_id = Column(Integer, ForeignKey("ninos.id", ondelete="CASCADE"), nullable=False)
    terapia_tipo = Column(String(100), nullable=False)  # 'lenguaje', 'conductual', etc.
    
    # Ranking de terapeutas (ordenados por score TOPSIS)
    ranking_terapeutas = Column(JSON, nullable=False)  # [{"terapeuta_id": 5, "score": 0.98, "criterios": {...}}]
    
    # Terapeuta seleccionado (puede ser el #1 o asignado manualmente)
    terapeuta_seleccionado_id = Column(Integer, ForeignKey("personal.id"))
    
    # Explicación generada por Gemini del por qué es el mejor
    explicacion_seleccion = Column(Text)
    
    # Criterios usados en TOPSIS
    criterios_usados = Column(JSON)  # {"experiencia": 0.3, "carga_trabajo": 0.2, ...}
    
    fecha_calculo = Column(DateTime, default=datetime.utcnow)
    activo = Column(Integer, default=1)
    
    # Relaciones
    nino = relationship("Nino", backref="asignaciones_topsis")
    terapeuta_seleccionado = relationship("Personal", backref="asignaciones_topsis")


