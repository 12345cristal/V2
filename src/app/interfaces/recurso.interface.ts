// src/app/interfaces/recurso.interface.ts

export interface TipoRecurso {
  id: number;
  codigo: string;
  nombre: string;
  descripcion?: string;
}

export interface CategoriaRecurso {
  id: number;
  codigo: string;
  nombre: string;
  descripcion?: string;
}

export interface NivelRecurso {
  id: number;
  codigo: string;
  nombre: string;
  orden: number;
}

export interface Recurso {
  id: number;
  personalId?: number;
  titulo: string;
  descripcion?: string;
  tipoId?: number;
  categoriaId?: number;
  nivelId?: number;
  etiquetas?: string[];
  archivoUrl?: string;
  esDestacado: number;
  fechaPublicacion: string;
  fechaModificacion: string;
  activo: number;
  // Información adicional
  personalNombre?: string;
  tipoNombre?: string;
  categoriaNombre?: string;
  nivelNombre?: string;
}

export interface RecursoListItem {
  id: number;
  titulo: string;
  descripcion?: string;
  tipoNombre?: string;
  categoriaNombre?: string;
  nivelNombre?: string;
  esDestacado: number;
  fechaPublicacion: string;
}

export interface RecursoCreate {
  personalId?: number;
  titulo: string;
  descripcion?: string;
  tipoId?: number;
  categoriaId?: number;
  nivelId?: number;
  etiquetas?: string[];
  archivoUrl?: string;
  esDestacado?: number;
}

export interface RecursoUpdate {
  titulo?: string;
  descripcion?: string;
  tipoId?: number;
  categoriaId?: number;
  nivelId?: number;
  etiquetas?: string[];
  archivoUrl?: string;
  esDestacado?: number;
  activo?: number;
}
