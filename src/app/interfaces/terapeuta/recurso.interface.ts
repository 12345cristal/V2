export interface Recurso {
  id: number;
  personal_id: number;
  titulo: string;
  descripcion: string;
  tipo_id: number;        // tipo_recurso
  categoria_id?: number; // categoria_recurso
  nivel_id?: number;     // nivel_recurso
  etiquetas?: string;
  es_destacado: boolean;
  es_nuevo: boolean;
  fecha_publicacion: string;
  ultima_actualizacion: string;
  total_asignaciones?: number;
  total_completadas?: number;
  rating_promedio?: number;
}
