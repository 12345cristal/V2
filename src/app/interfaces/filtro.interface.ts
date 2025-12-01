// src/app/shared/actividades/filtro.interface.ts

export interface OpcionFiltro {
  id: string;
  nombre: string;
}

export interface FiltrosActividad {
  tipos: OpcionFiltro[];
  categorias: OpcionFiltro[];
  niveles: OpcionFiltro[];
}
