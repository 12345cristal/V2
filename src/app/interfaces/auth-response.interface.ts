// src/app/auth/interfaces/auth-response.interface.ts
export interface AuthUser {
  id: number;
  rol_id: number;
  nombres: string;
  apellido_paterno: string;
  apellido_materno?: string;
  email: string;
}

export interface LoginResponse {
  access_token: string;
  user: AuthUser;
}
