// src/app/service/usuario.service.ts
import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../../environments/environment';

import type { UsuarioListado, Personal } from '../interfaces/usuario.interface';
import type { Rol } from '../interfaces/rol.interface';

/* =======================
   DTOs EXPORTADOS
======================= */
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
  activo?: boolean;
  password?: string;
}

@Injectable({ providedIn: 'root' })
export class UsuarioService {

  private readonly usuariosUrl =
    `${environment.apiBaseUrl}/usuarios`;

  private readonly personalSinUsuarioUrl =
    `${environment.apiBaseUrl}/personal/sin-terapia`;

  private readonly rolesUrl =
    `${environment.apiBaseUrl}/roles`;

  constructor(private http: HttpClient) {}

  getUsuarios(): Observable<UsuarioListado[]> {
    return this.http.get<UsuarioListado[]>(this.usuariosUrl);
  }

  getPersonalSinUsuario(): Observable<Personal[]> {
    return this.http.get<Personal[]>(this.personalSinUsuarioUrl);
  }

  getRoles(): Observable<Rol[]> {
    return this.http.get<Rol[]>(this.rolesUrl);
  }

  crearUsuario(payload: CrearUsuarioDto) {
    return this.http.post<UsuarioListado>(this.usuariosUrl, payload);
  }

  actualizarUsuario(id: number, payload: ActualizarUsuarioDto) {
    return this.http.put<UsuarioListado>(`${this.usuariosUrl}/${id}`, payload);
  }

  cambiarEstado(id: number, estado: 'ACTIVO' | 'INACTIVO') {
    return this.http.patch<UsuarioListado>(
      `${this.usuariosUrl}/${id}/estado`,
      { estado }
    );
  }
}
