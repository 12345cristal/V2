/**
 * Interfaces para el historial terapéutico y evolución
 */

/**
 * Historial terapéutico completo del niño
 */
export interface IHistorialTerapeutico {
  ninoId: number;
  nombreNino: string;
  fechaInicioTerapias: string;
  totalSesionesRealizadas: number;
  terapiasActivas: {
    tipo: string;
    terapeuta: string;
    fechaInicio: string;
    sesionesRealizadas: number;
  }[];
  terapiasCompletadas: {
    tipo: string;
    terapeuta: string;
    fechaInicio: string;
    fechaFin: string;
    totalSesiones: number;
    objetivosAlcanzados: number;
    objetivosTotales: number;
  }[];
  asistenciaPorMes: IAsistenciaMes[];
  evolucionObjetivos: IEvolucionObjetivos[];
  graficas: IGrafica[];
}

/**
 * Asistencia mensual a sesiones
 */
export interface IAsistenciaMes {
  mes: string; // formato: YYYY-MM
  mesNombre: string;
  sesionesAgendadas: number;
  sesionesAsistidas: number;
  sesionesCanceladas: number;
  sesionesNoAsistio: number;
  porcentajeAsistencia: number;
}

/**
 * Evolución de objetivos terapéuticos
 */
export interface IEvolucionObjetivos {
  id: number;
  ninoId: number;
  tipoTerapia: string;
  objetivo: string;
  descripcion?: string;
  fechaInicio: string;
  fechaObjetivoAlcanzado?: string;
  estado: 'EN_PROGRESO' | 'ALCANZADO' | 'PAUSADO' | 'DESCONTINUADO';
  progreso: number; // 0-100
  evaluaciones: {
    fecha: string;
    progreso: number;
    observaciones: string;
    evaluadoPor: string;
  }[];
  hitos: {
    fecha: string;
    descripcion: string;
    importancia: 'ALTA' | 'MEDIA' | 'BAJA';
  }[];
}

/**
 * Datos para gráficas de evolución
 */
export interface IGrafica {
  tipo: 'ASISTENCIA' | 'PROGRESO_OBJETIVOS' | 'COMPORTAMIENTO' | 'HABILIDADES';
  titulo: string;
  descripcion?: string;
  periodo: {
    inicio: string;
    fin: string;
  };
  datos: {
    etiqueta: string;
    valor: number;
    fecha?: string;
  }[];
  unidad?: string;
  colorGrafica?: string;
}
