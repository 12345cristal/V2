/**
 * Interfaces compartidas y comunes del módulo padre
 */

/**
 * Usuario del sistema
 */
export interface IUsuario {
  id: number;
  email: string;
  username: string;
  nombreCompleto: string;
  rol: 'PADRE' | 'TERAPEUTA' | 'COORDINADOR' | 'ADMINISTRADOR';
  foto?: string;
  telefono?: string;
  activo: boolean;
  verificado: boolean;
  fechaRegistro: string;
  ultimoAcceso?: string;
}

/**
 * Información del terapeuta
 */
export interface ITerapeuta {
  id: number;
  usuarioId: number;
  nombre: string;
  apellidos: string;
  nombreCompleto: string;
  especialidad: string;
  especialidades: string[];
  cedula?: string;
  email: string;
  telefono?: string;
  foto?: string;
  biografia?: string;
  experienciaAnios?: number;
  certificaciones?: string[];
  idiomas?: string[];
  horarioAtencion?: {
    dia: string;
    horaInicio: string;
    horaFin: string;
  }[];
  modalidades: ('PRESENCIAL' | 'VIRTUAL')[];
  ubicacion?: string;
  calificacion?: number;
  numeroEvaluaciones: number;
  pacientesActivos: number;
  disponible: boolean;
  activo: boolean;
}

/**
 * Información del coordinador
 */
export interface ICoordinador {
  id: number;
  usuarioId: number;
  nombre: string;
  apellidos: string;
  nombreCompleto: string;
  email: string;
  telefono?: string;
  foto?: string;
  area?: string;
  pacientesAsignados: number;
  activo: boolean;
}

/**
 * Información del administrador
 */
export interface IAdministrador {
  id: number;
  usuarioId: number;
  nombre: string;
  apellidos: string;
  nombreCompleto: string;
  email: string;
  telefono?: string;
  foto?: string;
  permisos: string[];
  superadmin: boolean;
  activo: boolean;
}

/**
 * Respuesta genérica del API
 */
export interface IResponse<T = any> {
  success: boolean;
  message: string;
  data?: T;
  errors?: string[];
  meta?: {
    timestamp: string;
    requestId?: string;
    version?: string;
  };
}

/**
 * Configuración de paginación
 */
export interface IPaginacion {
  page: number;
  pageSize: number;
  total: number;
  totalPages: number;
  hasNext: boolean;
  hasPrevious: boolean;
}

/**
 * Respuesta paginada del API
 */
export interface IResponsePaginado<T = any> extends IResponse<T[]> {
  pagination: IPaginacion;
}
