export interface SesionTerapia {
  id: number;
  ninoId: number;
  ninoNombre: string;

  tipoDescripcion: string;   // <-- el backend lo manda así
  estadoDescripcion: string; // <-- también viene así
  diaNombre: string;         // <-- igual viene así

  diaSemana: number;
  horaInicio: string;
  horaFin: string;

  sala?: string;

  esReposicion: boolean;
  puedeMarcarComoCompletada: boolean;
}



