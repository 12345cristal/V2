// src/app/service/usuario.service.ts
import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

import { environment } from 'src/environments/environment';

// Interfaces
import type {
  UsuarioListado,
  Personal
} from '../interfaces/usuario.interface';

import type { Rol } from '../interfaces/rol.interface';

// DTOs
export interface CrearUsuarioDto {
  id_personal: number;
  nombres: string;
  apellido_paterno: string;
  apellido_materno?: string;
  email: string;
  password: string;
  rol_id: number;
  telefono?: string;
}

export interface ActualizarUsuarioDto {
  email?: string;
  rol_id?: number;
  telefono?: string;
  activo?: boolean;
  password?: string;
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
  crearUsuario(payload: CrearUsuarioDto): Observable<UsuarioListado> {
    return this.http.post<UsuarioListado>(this.baseUrl, payload);
  }

  actualizarUsuario(id: number, payload: ActualizarUsuarioDto): Observable<UsuarioListado> {
    return this.http.put<UsuarioListado>(`${this.baseUrl}/${id}`, payload);
  }

  cambiarEstado(
    id: number,
    nuevoEstado: 'ACTIVO' | 'INACTIVO'
  ): Observable<UsuarioListado> {
    return this.http.patch<UsuarioListado>(`${this.baseUrl}/${id}/estado`, {
      estado: nuevoEstado,
    });
  }
}

