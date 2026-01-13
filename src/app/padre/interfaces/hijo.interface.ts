export interface Hijo {
  id: number;
  nombre: string;
  apellido_paterno: string;
  apellido_materno?: string;
  fecha_nacimiento: string;
  estado: 'ACTIVO' | 'BAJA_TEMPORAL' | 'INACTIVO';
  foto_url?: string;
}



