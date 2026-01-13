// src/app/coordinador/interfaces/usuario.interface.ts

import type { Personal as PersonalInterface } from './personal.interface';

export type EstadoUsuario = 'ACTIVO' | 'INACTIVO';

export interface Personal {
  id_personal: number;
  nombres: string;
  apellido_paterno: string;
  apellido_materno?: string;
  correo_personal?: string;
  telefono_personal?: string;
  id_rol?: number;
  nombre_rol?: string;
  especialidad_principal?: string;
  fecha_ingreso?: string | Date;
}

export interface UsuarioListado {
  id_usuario: number;
  id_personal: number;
  nombre_completo: string;
  email: string;
  rol_id: number;
  nombre_rol: string;
  estado: EstadoUsuario;
}

export interface Rol {
  id_rol: number;
  nombre_rol: string;
  descripcion?: string;
}

export interface CrearUsuarioDto {
  id_personal: number;

  nombres: string;
  apellido_paterno: string;
  apellido_materno?: string;

  email: string;
  password: string;

  rol_id: number;
}

export interface ActualizarUsuarioDto {
  email?: string;
  rol_id?: number;
  password?: string;
  estado?: EstadoUsuario;
}

export type { PersonalInterface };
