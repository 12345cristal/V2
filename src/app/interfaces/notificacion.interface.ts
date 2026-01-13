export type TipoNotificacionPadre =
  | 'NUEVA_TAREA'
  | 'MODIFICACION_TERAPIA'
  | 'SESION_REPROGRAMADA'
  | 'SESION_CANCELADA'
  | 'PAGO_PROXIMO'
  | 'PAGO_ATRASADO'
  | 'NUEVO_COMENTARIO'
  | 'NUEVO_RECURSO'
  | 'SESION_COMPLETADA'
  | 'INFORME_DISPONIBLE';

export type TipoNotificacionTerapeuta =
  | 'HORARIO_ACTUALIZADO'
  | 'NUEVA_JUNTA'
  | 'EVENTO_PROXIMO'
  | 'NUEVO_PACIENTE'
  | 'SESION_CANCELADA'
  | 'TAREA_COMPLETADA'
  | 'MENSAJE_COORDINADOR';

export interface NotificacionBase {
  id: number;
  usuarioId: number;
  mensaje: string;
  tipo: TipoNotificacionPadre | TipoNotificacionTerapeuta;
  fecha: string;
  leida: boolean;
  metadata?: {
    relacionadoId?: number;
    relacionadoTipo?: string;
    accion?: string;
    prioridad?: 'alta' | 'media' | 'baja';
  };
}

export interface NotificacionPadre extends NotificacionBase {
  hijoId: number;
  tipo: TipoNotificacionPadre;
}

export interface NotificacionTerapeuta extends NotificacionBase {
  tipo: TipoNotificacionTerapeuta;
}

export type Notificacion = NotificacionPadre | NotificacionTerapeuta;



