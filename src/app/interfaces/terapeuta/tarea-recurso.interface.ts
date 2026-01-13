export interface TareaRecurso {
  id: number;
  recurso_id: number;
  nino_id: number;
  asignado_por?: number; // personal_id
  fecha_asignacion: string;
  fecha_limite?: string;
  completado: boolean;
  comentarios_padres?: string;
  notas_terapeuta?: string;
}
