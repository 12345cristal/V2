// src/app/interfaces/recomendacion.interface.ts

/**
 * Interfaz para actividades
 */
export interface Actividad {
  id: number;
  nombre: string;
  descripcion?: string;
  objetivo?: string;
  materiales?: string;
  duracion_minutos: number;
  tags: string[];
  dificultad: number;
  area_desarrollo?: string;
  activo: number;
}

/**
 * Interfaz para recomendación de actividad
 */
export interface RecomendacionActividad {
  actividad_id: number;
  actividad_nombre?: string;  // Alias para nombre
  nombre: string;
  descripcion?: string;
  objetivo?: string;
  materiales?: string;
  duracion_minutos?: number;
  score: number;
  tags: string[];
  dificultad: number;
  nivel_dificultad?: string;  // Representación textual
  area_desarrollo?: string;
  categoria?: string;
  explicacion?: string;  // Explicación de Gemini AI
}

/**
 * Interfaz para historial de recomendaciones
 */
export interface HistorialRecomendacion {
  id: number;
  nino_id: number;
  actividad_id: number;
  actividad_nombre: string;
  fecha_recomendacion: string;
  aplicada: boolean;
  fecha_aplicacion?: string;
  score: number;
}

/**
 * Interfaz para recomendación de terapia
 */
export interface RecomendacionTerapia {
  terapia_id: number;
  nombre: string;
  descripcion?: string;
  score: number;
  categoria?: string;
  tags: string[];
}

