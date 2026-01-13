export interface AsistenciaPayload {
  sesion_id: number;
  asistio: boolean;
  observaciones?: string;
  progreso?: number;
  colaboracion?: number;
}
