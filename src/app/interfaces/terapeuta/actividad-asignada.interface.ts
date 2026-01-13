export interface ActividadAsignada {
  id: number;
  nino_id: number;
  nino_nombre: string;
  titulo: string;
  descripcion?: string;
  tipo: string;
  completada: boolean;
  fecha_limite?: string;
  created_at?: string;
  updated_at?: string;
}
