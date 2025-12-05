export interface RegistroAuditoria {
  id: number;
  fecha: string;          // ISO
  usuario: string;
  rol: string;
  modulo: string;         // 'TERAPIAS', 'NINOS', 'USUARIOS', etc.
  accion: string;         // 'CREATE', 'UPDATE', 'DELETE', 'LOGIN', ...
  descripcion: string;
  ip?: string | null;
}
