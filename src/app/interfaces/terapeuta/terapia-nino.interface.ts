export interface TerapiaNino {
  id: number;
  nino_id: number;
  terapia_id: number;
  terapeuta_id?: number;
  prioridad_id: number;
  frecuencia_semana: number;
  fecha_asignacion: string;
  activo: boolean;
}
