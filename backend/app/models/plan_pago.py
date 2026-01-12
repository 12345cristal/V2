# app/models/plan_pago.py
from sqlalchemy import Column, Integer, String, DECIMAL, Date, SmallInteger, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.base_class import Base


class PlanPago(Base):
    """
    Modelo para la tabla 'planes_pago'
    Planes de pago para los servicios del niño
    """
    __tablename__ = "planes_pago"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nino_id = Column(Integer, ForeignKey("ninos.id", ondelete="CASCADE"), nullable=False)
    
    nombre_plan = Column(String(200), nullable=False)  # Ej: "Terapia Mensual", "Plan Trimestral"
    monto_total = Column(DECIMAL(10, 2), nullable=False)
    
    # Control de abonos
    permite_abonos = Column(SmallInteger, default=1)  # 0 = pago único, 1 = permite abonos
    monto_pagado = Column(DECIMAL(10, 2), default=0.00)
    saldo_pendiente = Column(DECIMAL(10, 2))  # Se calcula: monto_total - monto_pagado
    
    # Fechas
    fecha_inicio = Column(Date, nullable=False)
    fecha_fin = Column(Date)
    fecha_creacion = Column(DateTime, default=datetime.utcnow)
    
    # Estado
    activo = Column(SmallInteger, default=1)  # 0 = inactivo/completado, 1 = activo
    estado = Column(String(50), default='PENDIENTE')  # PENDIENTE, EN_PROGRESO, COMPLETADO, CANCELADO

    # Relaciones
    nino = relationship("Nino", back_populates="planes_pago")
    pagos = relationship("Pago", back_populates="plan", cascade="all, delete-orphan")

    def calcular_saldo(self):
        """Calcula el saldo pendiente"""
        self.saldo_pendiente = float(self.monto_total) - float(self.monto_pagado)
        return self.saldo_pendiente

    def actualizar_monto_pagado(self, db):
        """Actualiza el monto pagado sumando todos los pagos asociados"""
        total_pagos = db.query(
            func.sum(Pago.monto)
        ).filter(
            Pago.plan_id == self.id,
            Pago.estado == 'COMPLETADO'
        ).scalar() or 0
        
        self.monto_pagado = total_pagos
        self.calcular_saldo()
        
        # Actualizar estado
        if self.saldo_pendiente <= 0:
            self.estado = 'COMPLETADO'
            self.activo = 0
        elif self.monto_pagado > 0:
            self.estado = 'EN_PROGRESO'


# Actualizar la relación en el modelo Nino
# Esto se debe agregar a app/models/nino.py:
# planes_pago = relationship("PlanPago", back_populates="nino", cascade="all, delete-orphan")
