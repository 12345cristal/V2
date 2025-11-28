export interface BitacoraEntrada {
  id: number;
  fecha: string;
  hora: string;

  comportamiento: string;       // Observaciones conductuales
  avance: string;               // Avance general
  actividadesRealizadas: string;
  recomendaciones: string;

  progresoSesion: number;       // 0–100
}
