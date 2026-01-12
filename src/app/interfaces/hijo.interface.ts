export interface Hijo {
  id: number;
  nombre: string;
  edad?: number;
  fechaNacimiento?: string; // ISO string para interoperar con API
  avatar?: string;
  diagnostico?: string;
}
