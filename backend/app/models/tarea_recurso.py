# app/models/tarea_recurso.py
from sqlalchemy import Column, Integer, String, Text, ForeignKey, SmallInteger, DateTime, Date
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.base_class import Base


class TareaRecurso(Base):
    """
    Modelo para la tabla 'tareas_recurso'
    Asignación de recursos educativos a niños por parte de terapeutas
    """
    __tablename__ = "tareas_recurso"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    recurso_id = Column(Integer, ForeignKey("recursos.id", ondelete="CASCADE"), nullable=False)
    nino_id = Column(Integer, ForeignKey("ninos.id", ondelete="CASCADE"), nullable=False)
    asignado_por = Column(Integer, ForeignKey("personal.id", ondelete="SET NULL"))
    
    # Fechas
    fecha_asignacion = Column(DateTime, default=datetime.utcnow, nullable=False)
    fecha_limite = Column(Date)
    fecha_completado = Column(DateTime)
    
    # Estado
    completado = Column(SmallInteger, default=0)  # 0 = pendiente, 1 = completado
    
    # Notas y comentarios
    comentarios_padres = Column(Text)  # Observaciones de los padres al completar
    notas_terapeuta = Column(Text)     # Instrucciones especiales del terapeuta
    
    # Evidencia (URL de archivos subidos por los padres)
    evidencia_url = Column(String(500))
    evidencia_tipo = Column(String(50))  # 'imagen', 'video', 'pdf'

    # Relaciones
    recurso = relationship("Recurso", back_populates="tareas_asignadas")
    nino = relationship("Nino", back_populates="tareas_recurso")
    asignador = relationship("Personal", foreign_keys=[asignado_por])


# Actualizar la relación en el modelo Nino
# Esto se debe agregar a app/models/nino.py:
# tareas_recurso = relationship("TareaRecurso", back_populates="nino", cascade="all, delete-orphan")
