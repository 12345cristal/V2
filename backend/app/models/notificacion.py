from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Text, SmallInteger
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.base_class import Base


class Notificacion(Base):
    """
    Modelo para la tabla 'notificaciones'
    Sistema de notificaciones para usuarios
    """
    __tablename__ = "notificaciones"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id", ondelete="CASCADE"), nullable=False, index=True)
    
    titulo = Column(String(200), nullable=False)
    mensaje = Column(Text, nullable=False)
    tipo = Column(String(50), nullable=False)  # 'TAREA', 'PAGO', 'CITA', 'GENERAL', etc.
    
    # Estado
    leida = Column(SmallInteger, default=0, nullable=False, index=True)  # 0 = no leída, 1 = leída
    
    # Fechas
    fecha = Column(DateTime, default=datetime.utcnow, nullable=False)
    fecha_leida = Column(DateTime)
    
    # Metadata adicional (JSON string para información extra)
    metadata_json = Column(Text)
    
    # Relaciones
    usuario = relationship("Usuario", back_populates="notificaciones")