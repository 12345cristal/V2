export interface Rol {
  id_rol: number;
  nombre_rol: string;
  descripcion?: string | null;
}

export type EstadoLaboral = 'ACTIVO' | 'VACACIONES' | 'INACTIVO';

export interface HorarioPersonal {
  id_horario?: number;
  dia_semana: number;      // 1=Lun ... 7=Dom
  hora_inicio: string;     // "09:00"
  hora_fin: string;        // "15:00"
}

export interface Personal {
  id_personal?: number;

  // Datos básicos
  nombres: string;
  apellido_paterno: string;
  apellido_materno?: string | null;

  id_rol: number;          // FK a roles
  especialidad_principal: string;

  // Contacto
  telefono_personal: string;
  correo_personal: string;

  // Datos laborales
  fecha_ingreso: string;   // ISO date (YYYY-MM-DD)
  estado_laboral: EstadoLaboral;

  // Métricas vistas en dashboard
 total_pacientes: number | null;
sesiones_semana: number | null;
rating: number | null;


  // Datos extra para el formulario (los que pediste)
  fecha_nacimiento: string;  // ISO date
  grado_academico: string;
  especialidades: string;    // lista separada por coma
  rfc: string;
  ine: string;
  curp: string;

  domicilio_calle: string;
  domicilio_colonia: string;
  domicilio_cp: string;
  domicilio_municipio: string;
  domicilio_estado: string;

  cv_archivo?: string | null;   // nombre/URL del CV
  experiencia: string;

  // Horarios
  horarios?: HorarioPersonal[];
}

