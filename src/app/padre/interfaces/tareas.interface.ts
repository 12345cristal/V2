/**
 * Interfaces para la gestión de tareas asignadas
 */

/**
 * Estados posibles de una tarea
 */
export enum IEstadoTarea {
  PENDIENTE = 'PENDIENTE',
  EN_PROGRESO = 'EN_PROGRESO',
  COMPLETADA = 'COMPLETADA',
  VENCIDA = 'VENCIDA',
  CANCELADA = 'CANCELADA'
}

/**
 * Tarea asignada al padre/niño
 */
export interface ITarea {
  id: number;
  ninoId: number;
  nombreNino: string;
  terapeutaId: number;
  nombreTerapeuta: string;
  sesionId?: number;
  titulo: string;
  descripcion: string;
  instrucciones?: string;
  objetivos?: string[];
  fechaAsignacion: string;
  fechaVencimiento?: string;
  diasRestantes?: number;
  estado: IEstadoTarea;
  prioridad: 'ALTA' | 'MEDIA' | 'BAJA';
  frecuencia?: 'DIARIA' | 'SEMANAL' | 'UNICA';
  duracionEstimada?: number; // en minutos
  recursosAsociados: IRecursoAsociado[];
  progresoReportado?: {
    fecha: string;
    descripcion: string;
    dificultades?: string;
    evidencia?: string[]; // URLs de fotos/videos
  }[];
  completada: boolean;
  fechaCompletado?: string;
  comentariosTerapeuta?: string;
  calificacion?: number; // 1-5
  notificacionesActivas: boolean;
}

/**
 * Recurso asociado a una tarea
 */
export interface IRecursoAsociado {
  id: number;
  tipo: 'DOCUMENTO' | 'VIDEO' | 'AUDIO' | 'IMAGEN' | 'ENLACE';
  titulo: string;
  descripcion?: string;
  url: string;
  nombreArchivo?: string;
  duracion?: number;
  obligatorio: boolean;
}
