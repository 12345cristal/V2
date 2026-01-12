export interface DocumentoPadre {
  key?: string | number;
  id: number;
  nombre: string;
  descripcion?: string;
  tipo: TipoDocumento;
  url: string;
  nuevo: boolean;
  visto: boolean;
  tamanioBytes?: number;
  fechaSubida: string;
  subidoPor?: string;
}

export interface DocumentoDetalle extends DocumentoPadre {
  tipoArchivo: string;
  fechaActualizacion: string;
  rutaDescarga: string;
}

export type TipoDocumento = 
  | 'ACUERDO_SERVICIOS'
  | 'REPORTE_TERAPEUTICO'
  | 'DOCUMENTO_MEDICO'
  | 'ACTUALIZACION_MEDICAMENTOS'
  | 'OTRO';

export interface RespuestaDocumentos {
  success: boolean;
  data?: DocumentoPadre[];
  error?: string;
  mensaje?: string;
  total?: number;
}
