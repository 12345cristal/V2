export interface Personal {
  id_personal: number;
id_usuario: number | null;

  // Datos de usuario (puedes adaptarlos a lo que devuelva tu API)
  nombre_completo: string;
  especialidad_principal?: string;

  fecha_nacimiento?: string | null;
  grado_academico?: string | null;
  especialidades?: string | null;
  telefono_personal?: string | null;
  correo_personal?: string | null;
  rfc?: string | null;
  ine?: string | null;
  curp?: string | null;
  domicilio_calle?: string | null;
  domicilio_colonia?: string | null;
  domicilio_cp?: string | null;
  domicilio_municipio?: string | null;
  domicilio_estado?: string | null;
  cv_archivo?: string | null;
  experiencia?: string | null;

  activo: boolean;
  calificacion_promedio?: number | null;

  creado_en?: string;
  actualizado_en?: string;
}

export type PersonalCreateDto = Omit<Personal, 'id_personal' | 'creado_en' | 'actualizado_en'> & {
  id_usuario: number | null;
};
export type PersonalUpdateDto = Partial<PersonalCreateDto>;
