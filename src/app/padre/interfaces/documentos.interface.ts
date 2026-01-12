/**
 * Interfaces para la gestión de documentos
 */

/**
 * Tipos de documento
 */
export enum ITipoDocumento {
  RECETA_MEDICA = 'RECETA_MEDICA',
  INDICACION_MEDICA = 'INDICACION_MEDICA',
  ESTUDIO = 'ESTUDIO',
  COMPROBANTE = 'COMPROBANTE',
  INFORME = 'INFORME',
  EVALUACION = 'EVALUACION',
  CONSENTIMIENTO = 'CONSENTIMIENTO',
  IDENTIFICACION = 'IDENTIFICACION',
  OTRO = 'OTRO'
}

/**
 * Documento del sistema
 */
export interface IDocumento {
  id: number;
  ninoId: number;
  nombreNino: string;
  titulo: string;
  descripcion?: string;
  tipo: ITipoDocumento;
  nombreArchivo: string;
  urlArchivo: string;
  tamanoBytes: number;
  mimeType: string;
  extension: string;
  subidoPor: 'PADRE' | 'TERAPEUTA' | 'COORDINADOR' | 'SISTEMA';
  subidoPorId: number;
  subidoPorNombre: string;
  parentesco?: 'MAMA' | 'PAPA' | 'TUTOR' | 'OTRO';
  fechaSubida: string;
  fechaDocumento?: string;
  vigenciaHasta?: string;
  visiblePara: {
    padres: boolean;
    terapeutas: boolean;
    coordinadores: boolean;
    administradores: boolean;
  };
  etiquetas?: string[];
  categorias?: string[];
  privado: boolean;
  visto: boolean;
  fechaVisto?: string;
  numeroDescargas: number;
  observaciones?: string;
  estado: 'ACTIVO' | 'ARCHIVADO' | 'ELIMINADO';
}
