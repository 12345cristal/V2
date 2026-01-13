export type EstadoCita = 'PROGRAMADA' | 'REALIZADA' | 'CANCELADA';

export interface EstadoCitaCatalogo {
  id: number;
  codigo: string;
  nombre: string;
}

export interface TerapiaBasica {
  id: number;
  nombre: string;
  descripcion?: string | null;
}

export interface Cita {
  id_cita: number;
  nino_id: number;
  terapeuta_id: number;
  terapia_id: number;
  fecha: string;  // YYYY-MM-DD
  hora_inicio: string;  // HH:mm:ss
  hora_fin: string;  // HH:mm:ss
  estado_id: number;
  motivo?: string | null;
  observaciones?: string | null;
  es_reposicion: number;
  // Campos calculados
  nino_nombre?: string | null;
  terapeuta_nombre?: string | null;
  terapia_nombre?: string | null;
  estado_nombre?: string | null;
}

export interface CitaCreate {
  nino_id: number;
  terapeuta_id: number;
  terapia_id: number;
  fecha: string;
  hora_inicio: string;
  hora_fin: string;
  estado_id?: number;
  motivo?: string;
  observaciones?: string;
  es_reposicion?: number;
}

export interface CitaUpdate {
  nino_id?: number;
  terapeuta_id?: number;
  terapia_id?: number;
  fecha?: string;
  hora_inicio?: string;
  hora_fin?: string;
  estado_id?: number;
  motivo?: string;
  observaciones?: string;
  es_reposicion?: number;
}

export interface CitaListResponse {
  items: Cita[];
  total: number;
  page: number;
  page_size: number;
}

export interface CitaFiltros {
  fecha?: string;
  nino_id?: number;
  terapeuta_id?: number;
  terapia_id?: number;
  estado_id?: number;
  buscar?: string;
  page?: number;
  page_size?: number;
}

