export type TipoDocumento =
  | 'RECETA_MEDICA'
  | 'INDICACION_MEDICA'
  | 'ESTUDIO'
  | 'COMPROBANTE'
  | 'INFORME'
  | 'OTRO';

export interface DocumentoBase {
  id: number;
  ninoId: number;
  titulo: string;
  descripcion?: string;
  fechaSubida: string;
  urlArchivo: string;
  nombreArchivo: string;
  tipo: TipoDocumento;
  subidoPor: 'PADRE' | 'TERAPEUTA' | 'CENTRO';
}

export interface DocumentoPadre extends DocumentoBase {
  subidoPor: 'PADRE';
  parentesco: 'MAMA' | 'PAPA' | 'TUTOR' | 'OTRO';
}

export interface DocumentoTerapeuta extends DocumentoBase {
  subidoPor: 'TERAPEUTA' | 'CENTRO';
}

export interface CrearDocumentoPadreDto {
  ninoId: number;
  titulo: string;
  descripcion?: string;
  tipo: TipoDocumento;
  parentesco: string;
  visibleParaTerapeutas: boolean;
  archivo: File;
}
