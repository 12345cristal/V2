// src/app/terapeuta/interfaces/dashboard-terapeuta.interface.ts

export type TipoNotificacion =
  | 'cambio-horario'
  | 'reposicion'
  | 'documento'
  | 'alerta';

export interface SesionDelDia {
  id_sesion: number;
  id_nino: number;

  nombre_nino: string;
  fotografia?: string;

  terapia: string;
  sala: string;
  es_reposicion: boolean;

  hora_inicio: string; // '09:00'
  hora_fin: string;    // '09:45'

  nota_importante?: string;
  tiene_retraso?: boolean;
}

export interface TareaRecurso {
  recurso: string;
  totalAsignados: number;
  completados: number;
}

export interface NotificacionDashboard {
  mensaje: string;
  fecha: string; // ISO o legible
  tipo: TipoNotificacion;
}

export interface HistorialSesionMini {
  fecha: string;
  terapia: string;
  resumen: string;
}

export interface IndicadoresNino {
  conducta: number;      // 0-100
  comunicacion: number;  // 0-100
  sensorial: number;     // 0-100
  autonomia?: number;    // opcional
}

export interface NinoAsignadoHoy {
  id_nino: number;
  nombre: string;
  fotografia?: string;
  edad?: number;  // Nueva propiedad
  nivelTEA?: number;  // 1, 2 o 3 - Nueva propiedad
  terapiaPrincipal: string;
  proximoHorario: string;
  cuatrimestreActual?: string;  // Nueva propiedad (ej: "Cuatrimestre 1 - 2025")
  ultimaSesion?: string;  // Nueva propiedad (fecha de última sesión)
  totalSesiones?: number;  // Nueva propiedad (total de sesiones realizadas)

  ultimasSesiones: HistorialSesionMini[];
  ultimaNotaClinica: string;
  progresoGeneral: string;      // 'En progreso', 'Mejorando', etc.
  indicadores: IndicadoresNino;
}

export interface EstadisticasSemanales {
  totalSesiones: number;
  asistenciasCompletadas: number;
  cancelaciones: number;
  reposicionesPendientes: number;
  satisfaccionPromedio?: number; // 0-5
}

export type EstadoLaboral = 'ACTIVO' | 'VACACIONES' | 'INACTIVO';

export interface ResumenDia {
  sesionesHoy: number;
  reposiciones: number;
  tareasPendientes: number;
}

export interface InfoTerapeuta {
  id_terapeuta: number;
  nombre: string;
  especialidad: string;
  estadoLaboral: EstadoLaboral;
  fechaHoy: string; // 'Viernes, 28 de noviembre de 2025'
}

export interface DashboardTerapeuta {
  terapeuta: InfoTerapeuta;
  resumen: ResumenDia;

  sesionesDelDia: SesionDelDia[];
  ninosAsignadosHoy: NinoAsignadoHoy[];

  tareasPendientes: TareaRecurso[];
  notificaciones: NotificacionDashboard[];
  estadisticasSemanales: EstadisticasSemanales;
}
