export interface Actividad {
  id: number;
  nino_id: number;
  nino_nombre: string;

  titulo: string;
  descripcion?: string;
  tipo: 'TAREA' | 'ARCHIVO';

  archivo_url?: string;
  completada: boolean;

  created_at: string;
}
