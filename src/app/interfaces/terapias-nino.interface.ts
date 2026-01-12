// src/app/interfaces/terapias-nino.interface.ts

export interface TerapiaNino {
  id: number;
  ninoId: number;
  terapiaId: number;
  terapeutaId?: number;
  prioridadId: number;
  frecuenciaSemana: number;
  fechaAsignacion?: string;
  activo: number;
  // Información adicional
  terapiaNombre?: string;
  terapiaDescripcion?: string;
  terapiaDuracion?: number;
  ninoNombre?: string;
  terapeutaNombre?: string;
  prioridadNombre?: string;
}

export interface TerapiaNinoCreate {
  ninoId: number;
  terapiaId: number;
  terapeutaId?: number;
  prioridadId: number;
  frecuenciaSemana: number;
  fechaAsignacion?: string;
}

export interface TerapiaNinoUpdate {
  terapeutaId?: number;
  prioridadId?: number;
  frecuenciaSemana?: number;
  activo?: number;
}

// Interfaces legacy para compatibilidad
export type TipoTerapiaNino =
  | 'LENGUAJE'
  | 'FISIOTERAPIA'
  | 'PSICOLOGIA'
  | 'OCUPACIONAL'
  | 'OTRA';

export interface NinoResumen {
  id_nino: number;
  nombre_completo: string;
  edad: number;
  diagnostico_principal?: string | null;
}

export interface TerapeutaResumenNino {
  id_terapeuta: number;
  nombre_completo: string;
  especialidad: string;
  correo?: string | null;
  telefono?: string | null;
}

export interface TerapiaAsignadaNino {
  id_terapia_nino: number;
  tipo_terapia: TipoTerapiaNino;
  area: string;
  terapeuta: TerapeutaResumenNino;
  frecuencia_semana: number;
  duracion_minutos: number;
  horario_resumen?: string | null;
  fecha_inicio: string;
  fecha_ultimo_reporte?: string | null;
  activo: boolean;
}

export interface NinoTerapiasDetalle {
  nino: NinoResumen;
  terapias: TerapiaAsignadaNino[];
}

