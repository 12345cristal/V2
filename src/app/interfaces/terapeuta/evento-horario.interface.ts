export interface EventoHorario {
  id_sesion: number;
  dia_semana: number;      // 1–7
  hora_inicio: string;     // HH:mm
  hora_fin: string;        // HH:mm
  nino_nombre: string;
  terapia_nombre: string;
  fecha: string;
  asistio: boolean;
}
