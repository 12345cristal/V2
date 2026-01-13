export type EstadoTerapia = 'ACTIVA' | 'INACTIVA';

export interface Terapia {
  id_terapia?: number;
  nombre: string;
  descripcion: string;
  estado: EstadoTerapia;
}

export interface AsignacionTerapia {
  id_asignacion?: number;
  id_personal: number;
  id_terapia: number;
}

export interface PersonalConTerapia {
  id_personal: number;
  nombre_completo: string;
  especialidad: string;
  id_terapia?: number | null;
}



