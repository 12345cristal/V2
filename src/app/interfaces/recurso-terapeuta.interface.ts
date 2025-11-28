// Interfaces del módulo de recursos del terapeuta

// Opción genérica para filtros (tipos, categorías, niveles, estados, etc.)
export interface OpcionFiltro {
  id: string;
  nombre: string;
}

// Datos que vienen del backend para llenar selects
export interface FiltrosRecurso {
  tipos: OpcionFiltro[];
  categorias: OpcionFiltro[];
  niveles: OpcionFiltro[];
  estados: OpcionFiltro[]; // si tu backend lo maneja, si no la puedes ignorar
}

// Recurso creado por el terapeuta
export interface RecursoTerapeuta {
  id: number;
  titulo: string;
  descripcion: string;

  tipoId: string;
  tipoNombre: string;

  categoriaId: string;
  categoriaNombre: string;

  nivelId: string;
  nivelNombre: string;

  etiquetas: string[];

  esDestacado: boolean;
  esNuevo: boolean;

  fechaPublicacion: string;      // ISO
  ultimaActualizacion: string;

  totalAsignaciones: number;
  totalCompletadas: number;
  ratingPromedio?: number | null;
}

// Niño disponible para asignar tareas
export interface NinoResumen {
  id: number;
  nombreCompleto: string;
  edad?: number;
  diagnosticoPrincipal?: string;
}

// Tarea asignada a los padres
export interface TareaAsignada {
  id: number;
  recursoId: number;

  ninoId: number;
  ninoNombre: string;

  tutorNombre: string;

  fechaAsignacion: string;
  fechaLimite?: string | null;

  completado: boolean;

  comentariosPadres?: string | null;
  notasTerapeuta?: string | null;
}

// DTOs para crear / actualizar desde el front
export interface CrearRecursoDto {
  titulo: string;
  descripcion: string;
  tipoId: string;
  categoriaId: string;
  nivelId: string;
  etiquetas: string[];
  esDestacado: boolean;
  esNuevo: boolean;
}

export interface ActualizarRecursoDto extends CrearRecursoDto {
  id: number;
}

export interface CrearTareaDto {
  recursoId: number;
  ninosIds: number[];
  fechaLimite?: string | null;
  notasTerapeuta?: string | null;
}

export interface ActualizarTareaDto {
  completado?: boolean;
  notasTerapeuta?: string | null;
}
