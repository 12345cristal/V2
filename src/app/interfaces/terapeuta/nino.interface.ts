export interface Nino {
  id: number;
  nombre: string;
  apellido_paterno: string;
  apellido_materno?: string;
  fecha_nacimiento: string; // YYYY-MM-DD
  sexo: 'M' | 'F' | 'O';
  curp?: string;
  tutor_id?: number;
  estado: 'ACTIVO' | 'BAJA_TEMPORAL' | 'INACTIVO';
  fecha_registro?: string;
  perfil_contenido?: any; // JSON del backend
}
