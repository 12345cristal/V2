# app/schemas/plan_pago.py
from pydantic import BaseModel, Field, field_validator
from typing import Optional
from datetime import date, datetime
from decimal import Decimal


class PlanPagoBase(BaseModel):
    nino_id: int
    nombre_plan: str = Field(..., min_length=1, max_length=200)
    monto_total: Decimal = Field(..., ge=0, decimal_places=2)
    permite_abonos: int = Field(default=1, ge=0, le=1)
    fecha_inicio: date
    fecha_fin: Optional[date] = None


class PlanPagoCreate(PlanPagoBase):
    pass


class PlanPagoUpdate(BaseModel):
    nombre_plan: Optional[str] = Field(None, min_length=1, max_length=200)
    monto_total: Optional[Decimal] = Field(None, ge=0, decimal_places=2)
    permite_abonos: Optional[int] = Field(None, ge=0, le=1)
    fecha_inicio: Optional[date] = None
    fecha_fin: Optional[date] = None
    activo: Optional[int] = Field(None, ge=0, le=1)
    estado: Optional[str] = None


class PlanPagoResponse(PlanPagoBase):
    id: int
    monto_pagado: Decimal
    saldo_pendiente: Optional[Decimal]
    fecha_creacion: datetime
    activo: int
    estado: str
    
    # Información adicional del niño
    nino_nombre: Optional[str] = None
    nino_apellido: Optional[str] = None
    
    # Estadísticas de pagos
    numero_pagos: Optional[int] = 0
    
    class Config:
        from_attributes = True


class PlanPagoListItem(BaseModel):
    """Versión simplificada para listados"""
    id: int
    nino_id: int
    nino_nombre: str
    nombre_plan: str
    monto_total: Decimal
    monto_pagado: Decimal
    saldo_pendiente: Optional[Decimal]
    estado: str
    activo: int
    fecha_inicio: date
    fecha_fin: Optional[date]
    
    class Config:
        from_attributes = True


class SaldoPendienteResponse(BaseModel):
    """Respuesta para cálculo de saldo pendiente"""
    plan_id: int
    monto_total: Decimal
    monto_pagado: Decimal
    saldo_pendiente: Decimal
    porcentaje_pagado: float
