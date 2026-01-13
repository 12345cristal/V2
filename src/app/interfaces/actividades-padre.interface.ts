// Interfaces específicas para el módulo de actividades del padre

// Actividad asignada que verá el padre
export interface ActividadAsignadaPadre {
  id: number;
  actividadId: number;

  // Niño
  ninoId: number;
  ninoNombre: string;

  // Información de la actividad
  actividadTitulo: string;
  actividadDescripcionCorta?: string | null;

  objetivoClinico?: string | null;
  instruccionesPadres?: string | null;
  materialRequerido?: string | null;
  duracionMinutos?: number | null;

  // Información de asignación
  fechaAsignacion: string;     // ISO
  fechaLimite?: string | null; // ISO o null

  // Estado
  completado: boolean;
  fechaCompletado?: string | null;

  // Comentarios y rating
  comentariosPadres?: string | null;
  ratingTutor?: number | null;   // 1-5
}

// DTO que envía el padre al marcar como completada
export interface CompletarActividadPadreDto {
  completado: boolean;
  comentariosPadres?: string | null;
}

// Rating al tutor / actividad
export interface CrearValoracionPadreDto {
  puntuacion: number;           // 1-5
  comentario?: string | null;
}

// Resumen para el encabezado
export interface ResumenActividadesPadre {
  totalPendientes: number;
  totalCompletadas: number;
  pendientesHoy: number;
}



