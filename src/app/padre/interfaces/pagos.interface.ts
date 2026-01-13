/**
 * Interfaces para la gestión de pagos y planes
 */

/**
 * Métodos de pago disponibles
 */
export enum IMetodoPago {
  EFECTIVO = 'EFECTIVO',
  TARJETA_CREDITO = 'TARJETA_CREDITO',
  TARJETA_DEBITO = 'TARJETA_DEBITO',
  TRANSFERENCIA = 'TRANSFERENCIA',
  PAYPAL = 'PAYPAL',
  MERCADO_PAGO = 'MERCADO_PAGO',
  OTRO = 'OTRO'
}

/**
 * Plan de terapias contratado
 */
export interface IPlan {
  id: number;
  ninoId: number;
  nombreNino: string;
  nombre: string;
  descripcion: string;
  tipoTerapias: string[];
  sesionesIncluidas: number;
  sesionesPorSemana: number;
  duracionMeses: number;
  precioMensual: number;
  precioTotal: number;
  moneda: string;
  descuento?: number;
  fechaInicio: string;
  fechaFin: string;
  estado: 'ACTIVO' | 'PAUSADO' | 'FINALIZADO' | 'CANCELADO';
  sesionesConsumidas: number;
  sesionesRestantes: number;
  renovacionAutomatica: boolean;
}

/**
 * Registro de un pago
 */
export interface IPago {
  id: number;
  ninoId: number;
  nombreNino: string;
  planId?: number;
  concepto: string;
  descripcion?: string;
  monto: number;
  moneda: string;
  metodoPago: IMetodoPago;
  fechaPago: string;
  fechaVencimiento?: string;
  estado: 'PENDIENTE' | 'PAGADO' | 'VENCIDO' | 'CANCELADO' | 'REEMBOLSADO';
  numeroTransaccion?: string;
  numeroRecibo?: string;
  urlComprobante?: string;
  procesadoPor?: string;
  notas?: string;
  sesionesAplicables?: number[];
  fechaRegistro: string;
}

/**
 * Historial completo de pagos
 */
export interface IHistorialPagos {
  ninoId: number;
  nombreNino: string;
  totalPagado: number;
  totalPendiente: number;
  moneda: string;
  pagos: IPago[];
  estadisticas: {
    pagosPuntuales: number;
    pagosAtrasados: number;
    promedioMensual: number;
    ultimoPago?: {
      fecha: string;
      monto: number;
    };
    proximoPago?: {
      fecha: string;
      monto: number;
    };
  };
}
