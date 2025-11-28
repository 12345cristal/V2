export interface SesionTerapia {
  id: number;
  ninoId: number;
  ninoNombre: string;

  tipoTerapia: string;         // "Lenguaje", "Ocupacional", etc.
  diaSemana: number;           // 1 = Lunes ... 7 = Domingo
  fecha?: string;              // opcional si es por fecha
  horaInicio: string;          // "09:00"
  horaFin: string;             // "10:00"
  sala?: string;

  esReposicion: boolean;
  estado: 'PROGRAMADA' | 'COMPLETADA' | 'CANCELADA';
}
