// src/app/coordinador/interfaces/usuario.interface.ts

import type { Personal } from './personal.interface';

export type EstadoUsuario = 'ACTIVO' | 'INACTIVO';

export interface UsuarioListado {
  id_usuario: number;
  id_personal?: number | null;

  email: string;
  username: string;
  nombre_completo: string;

  rol_id: number;
  nombre_rol: string;

  estado: EstadoUsuario;
  estado_laboral?: string | null;

  fecha_creacion?: string | null;
  ultima_sesion?: string | null;
}

export type { Personal };

