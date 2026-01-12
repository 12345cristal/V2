/**
 * Interfaces para el Dashboard del Padre
 * Contiene las estructuras de datos para la pantalla principal
 */

/**
 * Resumen general del dashboard
 */
export interface IDashboardResumen {
  totalHijos: number;
  sesionesEsteMes: number;
  proximaSesion?: IProximaSesion;
  ultimoAvance?: IUltimoAvance;
  pagosPendientes: number;
  documentosNuevos: number;
  observacionesPendientes: number;
}

/**
 * Información de la próxima sesión programada
 */
export interface IProximaSesion {
  id: number;
  ninoId: number;
  nombreNino: string;
  terapeutaId: number;
  nombreTerapeuta: string;
  tipoTerapia: string;
  fechaHora: string;
  duracion: number; // en minutos
  modalidad: 'PRESENCIAL' | 'VIRTUAL';
  ubicacion?: string;
  urlReunion?: string;
  observaciones?: string;
}

/**
 * Último avance registrado del niño
 */
export interface IUltimoAvance {
  id: number;
  ninoId: number;
  nombreNino: string;
  terapeutaId: number;
  nombreTerapeuta: string;
  fecha: string;
  titulo: string;
  descripcion: string;
  logros: string[];
  areasTrabajar: string[];
  calificacion?: number; // 1-5
}

/**
 * Información sobre pagos pendientes
 */
export interface IPagosPendientes {
  id: number;
  concepto: string;
  monto: number;
  moneda: string;
  fechaVencimiento: string;
  diasVencidos?: number;
  estado: 'PENDIENTE' | 'VENCIDO' | 'PARCIAL';
}

/**
 * Documento nuevo sin revisar
 */
export interface IDocumentoNuevo {
  id: number;
  titulo: string;
  tipo: string;
  fechaSubida: string;
  subidoPor: string;
  nombreArchivo: string;
  urlArchivo: string;
  visto: boolean;
}

/**
 * Observación del terapeuta
 */
export interface IObservacionTerapeuta {
  id: number;
  terapeutaId: number;
  nombreTerapeuta: string;
  ninoId: number;
  nombreNino: string;
  fecha: string;
  titulo: string;
  descripcion: string;
  prioridad: 'ALTA' | 'MEDIA' | 'BAJA';
  leida: boolean;
  requiereAccion: boolean;
}
