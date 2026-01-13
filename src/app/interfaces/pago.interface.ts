// src/app/interfaces/pago.interface.ts

export interface Pago {
  id: number;
  planId?: number;
  usuarioId?: number;
  monto: number;
  metodo?: string; // 'EFECTIVO', 'TRANSFERENCIA', 'TARJETA'
  referencia?: string;
  esAbono: number;
  fechaPago: string;
  fechaRegistro: string;
  comprobanteUrl?: string;
  estado: string; // 'COMPLETADO', 'PENDIENTE', 'RECHAZADO'
  observaciones?: string;
  // Información adicional
  planNombre?: string;
  ninoNombre?: string;
  usuarioNombre?: string;
}

export interface PagoListItem {
  id: number;
  planId?: number;
  planNombre?: string;
  monto: number;
  metodo?: string;
  fechaPago: string;
  estado: string;
  ninoNombre?: string;
}

export interface PagoCreate {
  planId?: number;
  usuarioId?: number;
  monto: number;
  metodo?: string;
  referencia?: string;
  esAbono?: number;
  comprobanteUrl?: string;
  observaciones?: string;
}

export interface PagoUpdate {
  metodo?: string;
  referencia?: string;
  estado?: string;
  comprobanteUrl?: string;
  observaciones?: string;
}

export interface HistorialPagos {
  pagos: PagoListItem[];
  totalPagos: number;
  montoTotal: number;
  ultimoPago?: string;
}

