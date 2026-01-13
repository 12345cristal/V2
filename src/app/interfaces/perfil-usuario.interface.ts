export type EstadoLaboral = 'ACTIVO' | 'VACACIONES' | 'INACTIVO';

export interface PerfilUsuario {
  id_personal: number;

  // Datos personales (mostrados desde personal)
  nombres: string;
  apellido_paterno: string;
  apellido_materno?: string | null;
  fecha_nacimiento?: string | null; // ISO 'YYYY-MM-DD'

  // Contacto (editable en personal_perfil)
  telefono_personal?: string | null;
  correo_personal?: string | null;

  // Profesión (editable en personal_perfil)
  grado_academico?: string | null;
  especialidad_principal?: string | null;
  especialidades?: string | null;  // lista tipo "Lenguaje, TEA, Conductual"
  experiencia?: string | null;     // descripción de experiencia

  // Domicilio (editable en personal_perfil)
  domicilio_calle?: string | null;
  domicilio_colonia?: string | null;
  domicilio_cp?: string | null;
  domicilio_municipio?: string | null;
  domicilio_estado?: string | null;

  // Documentos (en personal_perfil)
  foto_perfil?: string | null;      // URL relativa: fotos/personal_1_1700000000.png
  cv_archivo?: string | null;       // URL relativa: cv/personal_1_1700000000.pdf
  documentos_extra?: string[] | null;  // Lista de URLs relativas: ["documentos/...", ...]

  // Datos laborales (solo lectura desde personal)
  fecha_ingreso?: string | null;
  estado_laboral?: string | null;
  total_pacientes?: number | null;
  sesiones_semana?: number | null;
  rating?: number | null;
}



