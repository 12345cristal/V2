/**
 * Interfaces para el módulo TOPSIS de evaluación de terapeutas
 * Basado en Clean Architecture con validación de pesos
 */

/**
 * Pesos/ponderaciones para cada criterio de evaluación
 * Cada peso debe estar entre 0 y 1, y la suma total debe ser 1.0
 */
export interface PesosCriterios {
  carga_laboral: number;
  sesiones_completadas: number;
  rating: number;
  especialidad: number;
}

/**
 * Request para evaluación TOPSIS de terapeutas
 */
export interface TopsisEvaluacionRequest {
  terapia_id?: number;
  pesos: PesosCriterios;
  incluir_inactivos?: boolean;
}

/**
 * Métricas calculadas para un terapeuta
 */
export interface MetricasTerapeuta {
  carga_laboral: number;
  sesiones_completadas: number;
  rating: number;
  especialidad_match: boolean;
}

/**
 * Resultado individual de un terapeuta en el ranking
 */
export interface TerapeutaRanking {
  terapeuta_id: number;
  nombre: string;
  especialidad_principal: string | null;
  score: number;
  ranking: number;
  metricas: MetricasTerapeuta;
}

/**
 * Resultado completo de la evaluación TOPSIS
 */
export interface TopsisResultado {
  total_evaluados: number;
  terapia_solicitada: number | null;
  pesos_aplicados: PesosCriterios;
  ranking: TerapeutaRanking[];
}

/**
 * Configuración de pesos por defecto
 */
export interface PesosDefault {
  pesos: PesosCriterios;
  descripciones: {
    carga_laboral: string;
    sesiones_completadas: string;
    rating: string;
    especialidad: string;
  };
}

/**
 * Estado de carga del componente
 */
export interface EstadoCarga {
  cargando: boolean;
  error: string | null;
  mensajeInfo: string | null;
}
