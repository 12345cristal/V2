export interface Cita {
  id: number;
  nino_id: number;
  terapeuta_id: number;
  terapia_id: number;
  fecha: string; // YYYY-MM-DD
  hora_inicio: string;
  hora_fin: string;
  estado_id: number;
  confirmada: boolean;
}
