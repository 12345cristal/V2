export interface TerapeutaCargaDetalle {
  id_personal: number;
  nombre_completo: string;
  especialidad_principal: string;
  estado_laboral: 'ACTIVO' | 'VACACIONES' | 'INACTIVO';
  total_pacientes: number | null;
  sesiones_semana: number | null;
  rating: number | null;

  // Distribución de sesiones por terapia
  sesiones_por_terapia: {
    id_terapia: number;
    nombre_terapia: string;
    sesiones_semana: number;
  }[];

  // Horarios
  horarios: {
    dia_semana: number;   // 1-7
    hora_inicio: string;
    hora_fin: string;
  }[];

  // Historial breve de asignaciones
  historial_asignaciones: {
    id_terapia: number;
    nombre_terapia: string;
    fecha_asignacion: string;
    activo: boolean;
  }[];
}
