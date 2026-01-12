from pydantic import BaseModel
from typing import List, Optional
from datetime import date, time, datetime


# =============================
# HIJO
# =============================
class HijoOut(BaseModel):
    id: int
    nombre: str
    edad: int
    diagnostico: Optional[str]
    foto_url: Optional[str]


# =============================
# SESIÓN
# =============================
class SesionOut(BaseModel):
    fecha: date
    hora_inicio: time
    hora_fin: time
    terapia: str
    terapeuta: str
    estado: str


# =============================
# PROGRESO
# =============================
class ProgresoOut(BaseModel):
    sesiones_totales: int
    sesiones_completadas: int
    porcentaje: int


# =============================
# PAGOS
# =============================
class PagosResumenOut(BaseModel):
    monto_total: float
    monto_pagado: float
    monto_pendiente: float
    ultimo_pago_fecha: Optional[datetime]


# =============================
# ALERTAS
# =============================
class AlertasOut(BaseModel):
    documentos_nuevos: int
    medicamentos_nuevos: int
    recursos_nuevos: int


# =============================
# DASHBOARD PADRE
# =============================
class DashboardPadreOut(BaseModel):
    hijo: HijoOut
    sesiones_hoy: List[SesionOut]
    sesiones_semana: List[SesionOut]
    progreso: ProgresoOut
    pagos: PagosResumenOut
    alertas: AlertasOut
