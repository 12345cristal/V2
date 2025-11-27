// src/app/service/usuario.service.ts
import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

import { environment } from '../enviroment/environment';

// Interfaces
import type {
  Usuario,
  UsuarioListado,
  Personal
} from '../coordinador/interfaces/usuario.interface';

import type { Rol } from '../coordinador/interfaces/rol.interface';

// DTOs
export interface CrearUsuarioDto {
  id_personal: number;
  username: string;
  password: string;
  rol_sistema: string;
  debe_cambiar_password: boolean;
}

export interface ActualizarUsuarioDto {
  username: string;
  rol_sistema: string;
  estado: 'ACTIVO' | 'INACTIVO' | 'BLOQUEADO';
}

export interface CambiarPasswordDto {
  password: string;
  debe_cambiar_password: boolean;
}

@Injectable({
  providedIn: 'root',
})
export class UsuarioService {
  // ===========================
  // ENDPOINTS BASE
  // ===========================
  private baseUrl = environment.apiBaseUrl + environment.apiUsuarios;

  private personalSinUsuarioUrl =
    environment.apiBaseUrl + environment.apiPersonalSinUsuario;

  private rolesUrl =
    environment.apiBaseUrl + environment.apiRoles;  // 👈 NUEVO

  constructor(private http: HttpClient) {}

  // ===========================
  // LISTADOS
  // ===========================
  getUsuarios(): Observable<UsuarioListado[]> {
    return this.http.get<UsuarioListado[]>(this.baseUrl);
  }

  getPersonalSinUsuario(): Observable<Personal[]> {
    return this.http.get<Personal[]>(this.personalSinUsuarioUrl);
  }

  // === NUEVO: obtener roles desde la BD ===
  getRoles(): Observable<Rol[]> {
    return this.http.get<Rol[]>(this.rolesUrl);
  }

  // ===========================
  // CRUD
  // ===========================
  crearUsuario(payload: CrearUsuarioDto): Observable<Usuario> {
    return this.http.post<Usuario>(this.baseUrl, payload);
  }

  actualizarUsuario(id: number, payload: ActualizarUsuarioDto): Observable<Usuario> {
    return this.http.put<Usuario>(`${this.baseUrl}/${id}`, payload);
  }

  cambiarEstado(
    id: number,
    nuevoEstado: 'ACTIVO' | 'INACTIVO' | 'BLOQUEADO'
  ): Observable<Usuario> {
    return this.http.patch<Usuario>(`${this.baseUrl}/${id}/estado`, {
      estado: nuevoEstado,
    });
  }

  cambiarPassword(id: number, payload: CambiarPasswordDto): Observable<void> {
    return this.http.patch<void>(`${this.baseUrl}/${id}/password`, payload);
  }
}
