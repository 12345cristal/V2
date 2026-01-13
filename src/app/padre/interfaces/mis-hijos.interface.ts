/**
 * Interfaces para la gestión de información de los hijos
 */

/**
 * Información completa del hijo
 */
export interface IHijo {
  id: number;
  nombre: string;
  apellidos: string;
  nombreCompleto: string;
  fechaNacimiento: string;
  edad: number;
  genero: 'MASCULINO' | 'FEMENINO' | 'OTRO';
  fotoPerfil?: string;
  diagnostico?: string;
  fechaDiagnostico?: string;
  nivelSeveridad?: 'LEVE' | 'MODERADO' | 'SEVERO';
  alergias: IAlergias[];
  medicamentos: IMedicamento[];
  contactoEmergencia?: {
    nombre: string;
    telefono: string;
    relacion: string;
  };
  observaciones?: string;
  estado: 'ACTIVO' | 'INACTIVO';
  fechaRegistro: string;
}

/**
 * Información sobre alergias del niño
 */
export interface IAlergias {
  id: number;
  ninoId: number;
  tipo: 'ALIMENTO' | 'MEDICAMENTO' | 'AMBIENTAL' | 'OTRO';
  nombre: string;
  descripcion?: string;
  severidad: 'LEVE' | 'MODERADA' | 'SEVERA';
  reaccion?: string;
  fechaDeteccion?: string;
  activa: boolean;
}

/**
 * Medicamento que toma el niño
 */
export interface IMedicamento {
  id: number;
  ninoId: number;
  nombre: string;
  nombreComercial?: string;
  dosis: string;
  frecuencia: string;
  viaAdministracion: 'ORAL' | 'TOPICA' | 'INYECTABLE' | 'OTRA';
  horarios: string[];
  fechaInicio: string;
  fechaFin?: string;
  prescritoPor: string;
  indicaciones?: string;
  estado: IEstadoMedicamento;
  recordatorioActivo: boolean;
}

/**
 * Estado del medicamento
 */
export enum IEstadoMedicamento {
  ACTIVO = 'ACTIVO',
  SUSPENDIDO = 'SUSPENDIDO',
  COMPLETADO = 'COMPLETADO',
  PAUSADO = 'PAUSADO'
}
