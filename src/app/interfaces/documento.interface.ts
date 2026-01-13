export interface DocumentoPadre {
  id: number;
  nombre: string;
  titulo?: string;
  tipo?: string;
  fecha_creacion?: string;
  usuario_id?: number;
  visto?: boolean;
  url?: string;
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

