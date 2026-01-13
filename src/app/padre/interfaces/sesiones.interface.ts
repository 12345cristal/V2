/**
 * Interfaces para la gestión de sesiones terapéuticas
 */

/**
 * Tipos de terapia disponibles
 */
export enum ITipoTerapia {
  LENGUAJE = 'LENGUAJE',
  OCUPACIONAL = 'OCUPACIONAL',
  CONDUCTUAL = 'CONDUCTUAL',
  FISICA = 'FISICA',
  SENSORIAL = 'SENSORIAL',
  PSICOLOGIA = 'PSICOLOGIA',
  APRENDIZAJE = 'APRENDIZAJE',
  MUSICA = 'MUSICA',
  ARTE = 'ARTE',
  OTRA = 'OTRA'
}

/**
 * Estados posibles de una sesión
 */
export enum IEstadoSesion {
  PROGRAMADA = 'PROGRAMADA',
  CONFIRMADA = 'CONFIRMADA',
  EN_CURSO = 'EN_CURSO',
  COMPLETADA = 'COMPLETADA',
  CANCELADA = 'CANCELADA',
  REPROGRAMADA = 'REPROGRAMADA',
  NO_ASISTIO = 'NO_ASISTIO'
}

/**
 * Información completa de una sesión
 */
export interface ISesion {
  id: number;
  ninoId: number;
  nombreNino: string;
  terapeutaId: number;
  nombreTerapeuta: string;
  especialidadTerapeuta: string;
  tipoTerapia: ITipoTerapia;
  fechaHora: string;
  duracion: number; // en minutos
  modalidad: 'PRESENCIAL' | 'VIRTUAL';
  ubicacion?: string;
  urlReunion?: string;
  estado: IEstadoSesion;
  objetivos?: string[];
  materiales?: string[];
  observacionesPrevias?: string;
  bitacora?: IBitacoraDaily;
  grabaciones?: IGrabacionVoz[];
  asistencia?: {
    horaLlegada?: string;
    horaSalida?: string;
    confirmada: boolean;
  };
  costo?: number;
  pagado: boolean;
  motivoCancelacion?: string;
  fechaCancelacion?: string;
  fechaCreacion: string;
  fechaActualizacion?: string;
}

/**
 * Bitácora diaria de la sesión
 */
export interface IBitacoraDaily {
  id: number;
  sesionId: number;
  fecha: string;
  terapeutaId: number;
  actividadesRealizadas: string[];
  logros: string[];
  dificultades: string[];
  observaciones: string;
  estadoAnimico: 'MUY_BIEN' | 'BIEN' | 'NEUTRAL' | 'INQUIETO' | 'DIFICIL';
  participacion: 'ACTIVA' | 'MODERADA' | 'PASIVA' | 'RESISTENTE';
  recomendaciones?: string;
  tareasCasa?: string[];
  proximosObjetivos?: string[];
  firmaTerapeuta?: string;
  fechaRegistro: string;
}

/**
 * Grabación de voz de la sesión
 */
export interface IGrabacionVoz {
  id: number;
  sesionId: number;
  titulo: string;
  descripcion?: string;
  urlAudio: string;
  duracion: number; // en segundos
  fechaGrabacion: string;
  subidoPor: number;
  nombreSubidoPor: string;
  transcripcion?: string;
  notas?: string;
}
