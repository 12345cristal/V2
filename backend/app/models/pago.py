from sqlalchemy import Column, Integer, String, DECIMAL, DateTime, ForeignKey, SmallInteger, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.base_class import Base


class Pago(Base):
    """
    Modelo para la tabla 'pagos'
    Registro de pagos realizados por los tutores
    """
    __tablename__ = "pagos"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    plan_id = Column(Integer, ForeignKey("planes_pago.id", ondelete="CASCADE"))
    usuario_id = Column(Integer, ForeignKey("usuarios.id", ondelete="SET NULL"))  # Tutor que realizó el pago
    
    monto = Column(DECIMAL(10, 2), nullable=False)
    metodo = Column(String(50))  # 'EFECTIVO', 'TRANSFERENCIA', 'TARJETA', etc.
    referencia = Column(String(100))  # Número de referencia o transacción
    
    # Tipo de pago
    es_abono = Column(SmallInteger, default=1)  # 0 = pago único, 1 = abono parcial
    
    # Fechas
    fecha_pago = Column(DateTime, default=datetime.utcnow, nullable=False)
    fecha_registro = Column(DateTime, default=datetime.utcnow)
    
    # Comprobante
    comprobante_url = Column(String(500))  # URL del comprobante escaneado/foto
    
    # Estado
    estado = Column(String(50), default='COMPLETADO')  # COMPLETADO, PENDIENTE, RECHAZADO
    
    # Observaciones
    observaciones = Column(Text)
    
    # Relaciones
    plan = relationship("PlanPago", back_populates="pagos")
    usuario = relationship("Usuario", foreign_keys=[usuario_id])