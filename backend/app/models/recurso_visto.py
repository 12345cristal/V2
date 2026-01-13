from sqlalchemy import Column, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.base_class import Base

class RecursoVisto(Base):
    __tablename__ = "recursos_vistos"
    
    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"))
    recurso_id = Column(Integer, ForeignKey("recursos.id"))
    fecha_visto = Column(DateTime, default=datetime.utcnow)
    
    usuario = relationship("Usuario", back_populates="recursos_vistos")
    recurso = relationship("Recurso", back_populates="vistos_por")