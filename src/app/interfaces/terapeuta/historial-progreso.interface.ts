export interface HistorialProgreso {
  id: number;
  nino_id: number;
  actividad_id: number;
  terapeuta_id: number;
  calificacion?: number;
  notas_progreso?: string;
  fecha_sesion: string;
  duracion_minutos?: number;
  embedding_notas?: any; // JSON
  fecha_registro?: string;
}
