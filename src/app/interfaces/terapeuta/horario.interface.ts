export interface Horario {
  id: number;
  id_personal: number;
  dia_semana: number; // 1=Lunes ... 7=Domingo
  hora_inicio: string; // HH:mm:ss
  hora_fin: string;    // HH:mm:ss
}
