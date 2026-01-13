export interface Reporte {
  id: number;
  nino_id: number;
  tipo: 'SESION' | 'CUATRIMESTRAL';
  sesion_id?: number;
  periodo_inicio?: string;
  periodo_fin?: string;
  observaciones: string;
  fecha: string;
}
