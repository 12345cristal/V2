export type EstadoCita = 'AGENDADA' | 'COMPLETADA' | 'CANCELADA' | 'REPROGRAMADA';

export interface NinoResumen {
  id: number;
  nombreCompleto: string;
  tutorNombre: string;
  telefonoTutor1?: string | null;
  telefonoTutor2?: string | null;
}

export interface TerapiaBasica {
  id: number;
  nombre: string;
  descripcion?: string | null;
}

export interface EstadoCitaOpcion {
  id: number;
  codigo: EstadoCita;
  nombre: string;
  descripcion?: string | null;
}

export interface CitaListado {
  id: number;
  nombreNino: string;
  tutorNombre: string;
  telefonoTutor1?: string | null;
  telefonoTutor2?: string | null;
  fecha: string;
  horaInicio: string;
  horaFin: string;
  estado: EstadoCita;
  esReposicion: boolean;
  motivo: string;
  diagnosticoPresuntivo?: string | null;
  observaciones?: string | null;
}

export interface CrearCitaDto {
  nombreNino: string;
  tutorNombre: string;
  telefonoTutor1?: string | null;
  telefonoTutor2?: string | null;

  fecha: string;
  horaInicio: string;
  duracionMinutos: number;

  estadoId: number;
  esReposicion: boolean;
  citaOriginalId?: number | null;

  motivo: string;
  diagnosticoPresuntivo?: string | null;
  observaciones?: string | null;
}


export interface ActualizarCitaDto extends Partial<CrearCitaDto> {
  id: number;
}

export interface CatalogosCitaResponse {
  ninos: NinoResumen[];
  terapias: TerapiaBasica[];
  estadosCita: EstadoCitaOpcion[];
}
