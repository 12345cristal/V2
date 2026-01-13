/**
 * Interfaces para el sistema de notificaciones
 */

/**
 * Tipos de notificación
 */
export enum ITipoNotificacion {
  SESION_PROXIMA = 'SESION_PROXIMA',
  SESION_CANCELADA = 'SESION_CANCELADA',
  SESION_REPROGRAMADA = 'SESION_REPROGRAMADA',
  NUEVA_BITACORA = 'NUEVA_BITACORA',
  NUEVO_DOCUMENTO = 'NUEVO_DOCUMENTO',
  TAREA_ASIGNADA = 'TAREA_ASIGNADA',
  TAREA_VENCIDA = 'TAREA_VENCIDA',
  PAGO_PENDIENTE = 'PAGO_PENDIENTE',
  PAGO_CONFIRMADO = 'PAGO_CONFIRMADO',
  NUEVO_MENSAJE = 'NUEVO_MENSAJE',
  OBSERVACION_TERAPEUTA = 'OBSERVACION_TERAPEUTA',
  RECORDATORIO_MEDICAMENTO = 'RECORDATORIO_MEDICAMENTO',
  SISTEMA = 'SISTEMA',
  OTRO = 'OTRO'
}

/**
 * Estados de la notificación
 */
export enum IEstadoNotificacion {
  NO_LEIDA = 'NO_LEIDA',
  LEIDA = 'LEIDA',
  ARCHIVADA = 'ARCHIVADA',
  ELIMINADA = 'ELIMINADA'
}

/**
 * Notificación del sistema
 */
export interface INotificacion {
  id: number;
  usuarioId: number;
  tipo: ITipoNotificacion;
  titulo: string;
  mensaje: string;
  prioridad: 'ALTA' | 'MEDIA' | 'BAJA';
  estado: IEstadoNotificacion;
  leida: boolean;
  fechaLeida?: string;
  icono?: string;
  color?: string;
  accion?: {
    tipo: 'LINK' | 'MODAL' | 'ACCION';
    ruta?: string;
    parametros?: any;
    etiquetaBoton?: string;
  };
  relacionadoCon?: {
    tipo: 'SESION' | 'DOCUMENTO' | 'TAREA' | 'PAGO' | 'MENSAJE' | 'NINO';
    id: number;
    nombre?: string;
  };
  datosAdicionales?: any;
  enviadaPorEmail: boolean;
  enviadaPorSMS: boolean;
  enviadaPorPush: boolean;
  fechaEnvio: string;
  fechaExpiracion?: string;
  fechaCreacion: string;
}
