export interface DashboardPadre {
  hijo: {
    id: number;
    nombre: string;
    edad: number;
  };
  estadisticas: {
    actividadesCompletadas: number;
    actividadesTotales: number;
    progreso: number;
    racha: number;
  };
  actividadesRecientes: ActividadReciente[];
  proximasActividades: ProximaActividad[];
}

export interface ActividadReciente {
  id: number;
  nombre: string;
  fecha: Date;
  completada: boolean;
  puntuacion?: number;
}

export interface ProximaActividad {
  id: number;
  nombre: string;
  fechaProgramada: Date;
  tipo: string;
}