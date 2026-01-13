// src/app/interfaces/plan-pago.interface.ts

export interface PlanPago {
  id: number;
  ninoId: number;
  nombrePlan: string;
  montoTotal: number;
  permiteAbonos: number;
  montoPagado: number;
  saldoPendiente?: number;
  fechaInicio: string;
  fechaFin?: string;
  fechaCreacion: string;
  activo: number;
  estado: string; // 'PENDIENTE', 'EN_PROGRESO', 'COMPLETADO', 'CANCELADO'
  // Información adicional
  ninoNombre?: string;
  ninoApellido?: string;
  numeroPagos?: number;
}

export interface PlanPagoListItem {
  id: number;
  ninoId: number;
  ninoNombre: string;
  nombrePlan: string;
  montoTotal: number;
  montoPagado: number;
  saldoPendiente?: number;
  estado: string;
  activo: number;
  fechaInicio: string;
  fechaFin?: string;
}

export interface PlanPagoCreate {
  ninoId: number;
  nombrePlan: string;
  montoTotal: number;
  permiteAbonos?: number;
  fechaInicio: string;
  fechaFin?: string;
}

export interface PlanPagoUpdate {
  nombrePlan?: string;
  montoTotal?: number;
  permiteAbonos?: number;
  fechaInicio?: string;
  fechaFin?: string;
  activo?: number;
  estado?: string;
}

export interface SaldoPendiente {
  planId: number;
  montoTotal: number;
  montoPagado: number;
  saldoPendiente: number;
  porcentajePagado: number;
}



