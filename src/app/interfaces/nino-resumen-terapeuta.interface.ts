export interface TerapiaAsignada {
  id: number;
  tipoCodigo: string;          // Código de la BD, ej: "LENGUAJE"
  tipoDescripcion: string;     // Texto ya formateado desde la BD
  diaSemana: number;           // 1-7
  diaNombre: string;           // "Lunes", "Martes", etc. viene de la BD
  horaInicio: string;
  horaFin: string;
  sala?: string;
}

export interface ReposicionLigera {
  id: number;
  fecha: string;
  motivo: string;
  estadoCodigo: string;         // "PENDING", "APPROVED" ... viene de la BD
  estadoDescripcion: string;    // "Pendiente", "Aprobada" ... viene de la BD
}

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
    nivelComprensionDescripcion: string; // ya formateado desde la BD
  };

  terapiasAsignadas: TerapiaAsignada[];

  reposiciones: ReposicionLigera[];

  progresoGeneral?: number;
  ultimaSesionDescripcion?: string | null;   // Texto amigable desde la BD
  proximaSesionDescripcion?: string | null;  // idem, ya armado por el backend
}



