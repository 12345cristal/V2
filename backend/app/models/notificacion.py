from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Text, func
from sqlalchemy.orm import relationship
from app.db.base_class import Base

class Notificacion(Base):
    __tablename__ = "notificaciones"
    
    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id", ondelete="CASCADE"), nullable=False, index=True)
    hijo_id = Column(Integer, ForeignKey("pacientes.id", ondelete="CASCADE"), nullable=True)
    tipo = Column(String(50), nullable=False)
    mensaje = Column(Text, nullable=False)
    leida = Column(Boolean, default=False, nullable=False, index=True)
    metadata_json = Column(Text, nullable=True)
    fecha_creacion = Column(DateTime, server_default=func.now(), nullable=False)
    
    # Relaciones
    usuario = relationship("Usuario", back_populates="notificaciones")
    hijo = relationship("Paciente", foreign_keys=[hijo_id])