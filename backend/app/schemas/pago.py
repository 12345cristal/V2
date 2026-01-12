# app/schemas/pago.py
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from decimal import Decimal


class PagoBase(BaseModel):
    plan_id: Optional[int] = None
    monto: Decimal = Field(..., ge=0, decimal_places=2)
    metodo: Optional[str] = Field(None, max_length=50)
    referencia: Optional[str] = Field(None, max_length=100)
    es_abono: int = Field(default=1, ge=0, le=1)
    observaciones: Optional[str] = None


class PagoCreate(PagoBase):
    usuario_id: Optional[int] = None
    comprobante_url: Optional[str] = None


class PagoUpdate(BaseModel):
    metodo: Optional[str] = Field(None, max_length=50)
    referencia: Optional[str] = Field(None, max_length=100)
    estado: Optional[str] = None
    comprobante_url: Optional[str] = None
    observaciones: Optional[str] = None


class PagoResponse(PagoBase):
    id: int
    usuario_id: Optional[int]
    fecha_pago: datetime
    fecha_registro: datetime
    comprobante_url: Optional[str]
    estado: str
    
    # Información adicional del plan
    plan_nombre: Optional[str] = None
    nino_nombre: Optional[str] = None
    
    # Información del usuario que pagó
    usuario_nombre: Optional[str] = None
    
    class Config:
        from_attributes = True


class PagoListItem(BaseModel):
    """Versión simplificada para listados"""
    id: int
    plan_id: Optional[int]
    plan_nombre: Optional[str]
    monto: Decimal
    metodo: Optional[str]
    fecha_pago: datetime
    estado: str
    nino_nombre: Optional[str]
    
    class Config:
        from_attributes = True


class HistorialPagosResponse(BaseModel):
    """Historial de pagos con resumen"""
    pagos: list[PagoListItem]
    total_pagos: int
    monto_total: Decimal
    ultimo_pago: Optional[datetime] = None
