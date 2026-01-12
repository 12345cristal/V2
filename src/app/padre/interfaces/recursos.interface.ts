/**
 * Interfaces para la gestión de recursos educativos
 */

/**
 * Tipos de recurso disponibles
 */
export enum ITipoRecurso {
  VIDEO = 'VIDEO',
  AUDIO = 'AUDIO',
  DOCUMENTO = 'DOCUMENTO',
  INFOGRAFIA = 'INFOGRAFIA',
  GUIA = 'GUIA',
  EJERCICIO = 'EJERCICIO',
  JUEGO = 'JUEGO',
  ACTIVIDAD = 'ACTIVIDAD',
  ARTICULO = 'ARTICULO',
  LIBRO = 'LIBRO',
  ENLACE = 'ENLACE',
  OTRO = 'OTRO'
}

/**
 * Recurso educativo o material de apoyo
 */
export interface IRecurso {
  id: number;
  titulo: string;
  descripcion: string;
  tipo: ITipoRecurso;
  categoria?: string;
  subcategoria?: string;
  urlRecurso: string;
  urlMiniatura?: string;
  nombreArchivo?: string;
  tamanoBytes?: number;
  duracion?: number; // en segundos para videos/audios
  autor?: string;
  fuenteOriginal?: string;
  idioma: string;
  edadRecomendada?: {
    min: number;
    max: number;
  };
  nivelDificultad?: 'BASICO' | 'INTERMEDIO' | 'AVANZADO';
  areasDesarrollo?: string[];
  etiquetas: string[];
  habilidadesObjetivo?: string[];
  materialNecesario?: string[];
  tiempoEstimado?: number; // en minutos
  instrucciones?: string;
  objetivosAprendizaje?: string[];
  recomendadoPor?: number;
  nombreRecomendadoPor?: string;
  calificacion?: number; // 1-5
  numeroCalificaciones: number;
  numeroDescargas: number;
  numeroVisualizaciones: number;
  favorito: boolean;
  completado: boolean;
  fechaCompletado?: string;
  progreso?: number; // 0-100
  notas?: string;
  fechaPublicacion: string;
  fechaActualizacion?: string;
  activo: boolean;
}
