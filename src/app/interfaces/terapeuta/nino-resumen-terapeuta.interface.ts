export interface NinoResumenTerapeuta {
  id: number;
  nombre: string;
  apellido_paterno: string;
  apellido_materno?: string;

  /** Derivado en frontend */
  nombreCompleto: string;
}
