// src/app/coordinador/interfaces/usuario.interface.ts

import type { Personal } from './personal.interface';

export type EstadoUsuario = 'ACTIVO' | 'INACTIVO' | 'BLOQUEADO';

export interface Usuario {
  id_usuario?: number;
  id_personal: number;

  username: string;
  rol_sistema: string;
  estado: EstadoUsuario;

  debe_cambiar_password?: boolean;

  fecha_creacion?: string;
  ultima_sesion?: string | null;
}

export interface UsuarioListado extends Usuario {
  nombre_completo: string;
  nombre_rol_personal?: string;
  estado_laboral?: string;
}

// exportar tipo correctamente
export type { Personal };
