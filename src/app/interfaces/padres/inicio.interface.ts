// padres/interfaces/inicio.interface.ts
export interface InicioPadre {
  hijo_id: string;
  hijo_nombre: string;

  proxima_sesion: {
    fecha: string;
    hora: string;
    terapeuta: string;
    tipo: string;
  } | null;

  ultimo_avance: {
    fecha: string;
    descripcion: string;
    porcentaje: number;
  } | null;

  pagos_pendientes: number;
  documento_nuevo: boolean;

  ultima_observacion: {
    fecha: string;
    terapeuta: string;
    resumen: string;
  } | null;
}
