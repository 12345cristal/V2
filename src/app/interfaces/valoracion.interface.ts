export interface CrearValoracionDto {
  puntuacion: number;
  comentario?: string | null;
}

export interface ValoracionActividad {
  id: number;
  asignacionId: number;
  puntuacion: number;
  comentario?: string | null;
  fecha: string;
}
