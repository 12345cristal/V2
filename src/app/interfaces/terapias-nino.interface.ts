// src/app/terapias/interfaces/terapias-nino.interface.ts

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
  area: string; // ejemplo: "Lenguaje", "Fisioterapia", "Psicología"
  terapeuta: TerapeutaResumenNino;
  frecuencia_semana: number;      // veces por semana
  duracion_minutos: number;       // duración de cada sesión
  horario_resumen?: string | null; // ej: "Lunes y Miércoles · 16:00 - 17:00"
  fecha_inicio: string;           // ISO string
  fecha_ultimo_reporte?: string | null;
  activo: boolean;
}

export interface NinoTerapiasDetalle {
  nino: NinoResumen;
  terapias: TerapiaAsignadaNino[];
}
