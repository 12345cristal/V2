export interface NinoResumenTerapeuta {
  id: number;

  nombreCompleto: string;
  edad: number;
  fotografiaUrl?: string;

  diagnosticoPrincipal: string;

  infoEmocional: {
    estimulosAnsiedad: string;
    cosasQueCalman: string;
    preferenciasSensoriales: string;
    palabrasClave: string;
    nivelComprension: 'ALTO' | 'MEDIO' | 'BAJO';
  };

  terapiaAsignada: {
    tipo: string;         // "Lenguaje", "Conductual"...
    diaSemana: number;    // 1–7
    horaInicio: string;   // "09:00"
    horaFin: string;      // "10:00"
    sala?: string;
  }[];

  reposiciones: {
    id: number;
    fecha: string;
    motivo: string;
    estado: 'PENDIENTE' | 'APROBADA' | 'RECHAZADA';
  }[];

  progresoGeneral?: number;
  ultimaSesion?: string | null;
  proximaSesion?: string | null;
}
