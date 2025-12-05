export interface TerapeutaRecomendado {
  id_personal: number;
  nombre_completo: string;
  score: number;          // siempre número
  rank: number;
  id_terapia: number;
  terapia_nombre: string;
  criterios: {
    rating: number;
    carga: number;
    sesiones: number;
    afinidad: number;
  };
}
