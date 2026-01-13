export interface BitacoraEntrada {
  id: number;
  fecha: string;
  hora: string;

  comportamiento: string;
  avance: string;
  actividadesRealizadas: string;
  recomendaciones: string;

  progresoSesion: number;

  cumplioObjetivos: boolean;
  requiereSeguimiento: boolean;

  etiquetas?: string[];         // Ej: ["Crisis leve", "Mejora atención"]
}

export interface BitacoraResultado {
  exito: boolean;
  mensaje: string;        // "Sesión registrada, faltaron X objetivos..."
  advertencias?: string[]; // Cosas que NO se cumplieron, viene de la BD
  entrada?: BitacoraEntrada;
}

