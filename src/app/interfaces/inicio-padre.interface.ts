// src/app/padres/interfaces/inicio-padre.interface.ts

export interface NinoResumenPadre {
  id: number;
  nombre: string;
  edad: number;
  fotoUrl?: string | null;
}

export type EstadoTerapia = 'POR_INICIAR' | 'EN_CURSO' | 'FINALIZADA';

export interface TerapiaDelDia {
  id: number;
  tipo: string;               // Ej: "Terapia del lenguaje"
  horaInicio: string;         // "16:00"
  horaFin: string;            // "17:00"
  terapeutaNombre: string;
  sala: string;
  estado: EstadoTerapia;
}

export type TipoActividad =
  | 'TAREA_CASA'
  | 'DOCUMENTO'
  | 'CUESTIONARIO'
  | 'OTRA';

export interface ActividadPendiente {
  id: number;
  titulo: string;
  tipo: TipoActividad;
  descripcionCorta: string;
  fechaLimite: string;        // ISO o "2025-12-01"
  prioridad: 'BAJA' | 'MEDIA' | 'ALTA';
  completado: boolean;
}

export interface InicioPadreResumen {
  nino: NinoResumenPadre;
  terapiaDeHoy: TerapiaDelDia | null;
  actividadesPendientes: ActividadPendiente[];
  mensajeDelDia?: string;
}

