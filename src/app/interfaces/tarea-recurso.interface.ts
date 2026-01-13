// src/app/interfaces/tarea-recurso.interface.ts

export interface TareaRecurso {
  id: number;
  recursoId: number;
  ninoId: number;
  asignadoPor?: number;
  fechaAsignacion: string;
  fechaLimite?: string;
  fechaCompletado?: string;
  completado: number;
  comentariosPadres?: string;
  notasTerapeuta?: string;
  evidenciaUrl?: string;
  evidenciaTipo?: string;
  // Información adicional
  recursoTitulo?: string;
  recursoDescripcion?: string;
  recursoArchivoUrl?: string;
  recursoTipo?: string;
  ninoNombre?: string;
  ninoApellido?: string;
  asignadorNombre?: string;
}

export interface TareaRecursoListItem {
  id: number;
  recursoId: number;
  recursoTitulo: string;
  recursoTipo?: string;
  ninoId: number;
  ninoNombre: string;
  fechaAsignacion: string;
  fechaLimite?: string;
  completado: number;
  asignadorNombre?: string;
}

export interface TareaRecursoCreate {
  recursoId: number;
  ninoId: number;
  asignadoPor?: number;
  fechaLimite?: string;
  notasTerapeuta?: string;
}

export interface TareaRecursoUpdate {
  fechaLimite?: string;
  notasTerapeuta?: string;
  completado?: number;
  comentariosPadres?: string;
}

export interface TareaRecursoMarcarCompletada {
  comentariosPadres?: string;
  evidenciaUrl?: string;
  evidenciaTipo?: string;
}

export interface EstadisticasTareas {
  total: number;
  pendientes: number;
  completadas: number;
  vencidas: number;
  porcentajeCompletadas: number;
}

