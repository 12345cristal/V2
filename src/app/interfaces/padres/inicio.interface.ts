export interface Hijo {
  id: string;
  nombre: string;
  edad: number;
  fotoPerfil?: string;
  estado: 'activo' | 'inactivo';
}

export interface ProximaSesion {
  id: string;
  fecha: string;
  hora: string;
  tipo: string;
  terapeuta: string;
  estado: 'pendiente' | 'completada' | 'cancelada';
}

export interface UltimoAvance {
  id: string;
  fecha: string;
  descripcion: string;
  porcentaje: number;
  area: string;
}

export interface UltimaObservacion {
  id: string;
  fecha: string;
  terapeuta: string;
  resumen: string;
}

export interface InicioPadre {
  hijoSeleccionado: Hijo;
  hijosActivos: Hijo[];
  proximaSesion?: ProximaSesion;
  ultimoAvance?: UltimoAvance;
  pagosPendientes: number;
  documentosNuevos: number;
  ultimaObservacion?: UltimaObservacion;
  porcentajeProgreso: number;
}
