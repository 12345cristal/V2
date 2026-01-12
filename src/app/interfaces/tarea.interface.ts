export interface TareaPadre {
  id: number;
  hijoId: number;
  objetivo: string;
  instrucciones: string;
  terapeuta: string;
  fechaAsignacion: string; // ISO
  fechaLimite?: string; // ISO
  estado: 'PENDIENTE' | 'REALIZADA' | 'VENCIDA';
  recursos: RecursoTarea[];
  evidencia?: EvidenciaTarea;
  observaciones?: string;
}

export interface RecursoTarea {
  id: number;
  titulo: string;
  tipo: 'PDF' | 'IMAGEN' | 'VIDEO' | 'ENLACE';
  url: string;
  nombreArchivo?: string;
}

export interface EvidenciaTarea {
  id: number;
  tipo: 'PDF' | 'IMAGEN';
  url: string;
  nombreArchivo: string;
  fechaSubida: string; // ISO
}

export interface TareaCreateDto {
  hijoId: number;
  objetivo: string;
  instrucciones: string;
  terapeutaId: number;
  fechaLimite?: string;
}

export interface MarcarRealizadaDto {
  observaciones?: string;
  evidenciaArchivo?: File;
}