from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Enum, Text, func
from sqlalchemy.orm import relationship
from app.db.base_class import Base
import enum

class EstadoPago(enum.Enum):
    pagado = "pagado"
    pendiente = "pendiente"
    atrasado = "atrasado"
    cancelado = "cancelado"

class Pago(Base):
    __tablename__ = "pagos"
    
    id = Column(Integer, primary_key=True, index=True)
    padre_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False, index=True)
    hijo_id = Column(Integer, ForeignKey("pacientes.id", ondelete="CASCADE"), nullable=False, index=True)
    monto = Column(Float, nullable=False)
    concepto = Column(String(255), nullable=False)
    estado = Column(Enum(EstadoPago), default=EstadoPago.pendiente, nullable=False, index=True)
    fecha_vencimiento = Column(DateTime, nullable=False)
    fecha_pago = Column(DateTime, nullable=True)
    metodo_pago = Column(String(50), nullable=True)
    referencia = Column(String(255), nullable=True)
    observaciones = Column(Text, nullable=True)
    fecha_creacion = Column(DateTime, server_default=func.now())
    
    padre = relationship("Usuario", foreign_keys=[padre_id])
    hijo = relationship("Paciente", back_populates="pagos")