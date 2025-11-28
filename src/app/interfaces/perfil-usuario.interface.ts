export type EstadoLaboral = 'ACTIVO' | 'VACACIONES' | 'INACTIVO';

export interface PerfilUsuario {
  id_personal: number;

  // Datos personales (solo lectura en el perfil)
  nombres: string;
  apellido_paterno: string;
  apellido_materno?: string | null;
  fecha_nacimiento: string; // ISO 'YYYY-MM-DD'

  // Contacto (editable)
  telefono_personal: string;
  correo_personal: string;

  // Profesión (editable parcialmente)
  grado_academico: string;
  especialidad_principal: string;
  especialidades: string;  // lista tipo "Lenguaje, TEA, Conductual"
  experiencia: string;

  // Domicilio (editable)
  domicilio_calle: string;
  domicilio_colonia: string;
  domicilio_cp: string;
  domicilio_municipio: string;
  domicilio_estado: string;

  // Documentos
  cv_archivo?: string | null;   // URL o nombre del archivo

  // Datos laborales (solo lectura, opcionales)
  fecha_ingreso?: string;      // ISO
  estado_laboral?: EstadoLaboral;
  total_pacientes?: number | null;
  sesiones_semana?: number | null;
  rating?: number | null;
}
