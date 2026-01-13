export interface Actividad {
  id: number;
  nombre: string;
  descripcion?: string;
  objetivo?: string;
  materiales?: string;
  duracion_minutos: number;
  tags?: string[]; // viene de JSON
  dificultad: 1 | 2 | 3;
  area_desarrollo?: string; // cognitivo, motor, lenguaje, etc.
  activo: boolean;
  created_at?: string;
  updated_at?: string;
}
