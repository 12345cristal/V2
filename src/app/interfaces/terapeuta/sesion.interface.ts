export interface Sesion {
  id: number;
  terapia_nino_id: number;
  fecha: string; // datetime
  asistio: boolean;
  progreso?: number;
  colaboracion?: number;
  observaciones?: string;
  creado_por?: number; // personal_id
}
