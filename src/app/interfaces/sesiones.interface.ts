export interface Sesion {
  id: number;
  hijoId: number;
  tipoTerapia: string;
  fecha: string; // ISO date o "DD/MM/YYYY"
  horaInicio: string; // HH:mm
  horaFin: string; // HH:mm
  terapeuta?: string;
  estado: 'completada' | 'pendiente' | 'cancelada' | 'reprogramada';
  puntuacion?: number;
}

export interface SesionDetalle {
  id: number;
  hijoId: number;
  tipoTerapia: string;
  fecha: string;
  horaInicio: string;
  horaFin: string;
  terapeuta?: string;
  estado: 'completada' | 'pendiente' | 'cancelada' | 'reprogramada';
  comentarios?: string;
  grabacionUrl?: string;
  bitacoraUrl?: string;
  actividades: Actividad[];
  puntuacion?: number;
}

export interface Actividad {
  id: number;
  nombre: string;
  descripcion?: string;
  completada: boolean;
  observaciones?: string;
}
