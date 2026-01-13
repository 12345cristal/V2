export interface RecomendacionActividad {
  id: number;
  nino_id: number;
  actividades_recomendadas: number[]; // IDs de actividades
  explicacion_humana?: string;
  metodo: 'CONTENT_BASED' | 'TOPSIS' | 'MANUAL';
  fecha_generacion: string;
  aplicada: boolean;
}
