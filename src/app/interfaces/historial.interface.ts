export interface HistorialResumen {
  hijoId: number;
  periodo: string; // "2025" o "Últimos 6 meses"
  asistenciaMensual: AsistenciaMes[];
  sesionesVsCanceladas: SesionesVsCanceladas;
  evolucionObjetivos: EvolucionObjetivo[];
  frecuenciaTerapias: FrecuenciaTerapia[];
  estadisticasGenerales: EstadisticasGenerales;
}

export interface AsistenciaMes {
  mes: string; // "Enero 2025", "Febrero 2025"
  asistidas: number;
  canceladas: number;
  porcentajeAsistencia: number;
}

export interface SesionesVsCanceladas {
  realizadas: number;
  canceladas: number;
  porcentajeRealizacion: number;
}

export interface EvolucionObjetivo {
  fecha: string; // "2025-01-01"
  objetivo: string;
  valor: number; // 0-5
  observaciones?: string;
}

export interface FrecuenciaTerapia {
  terapia: string;
  sesionesPorSemana: number;
  totalSesiones: number;
}

export interface EstadisticasGenerales {
  duracionPromedio: number; // minutos
  terapeuta: string;
  inicioTerapia: string; // fecha ISO
  evaluacionGeneral: number; // 0-10
}

