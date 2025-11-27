import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { PerfilUsuario } from '../coordinador/interfaces/perfil-usuario.interface';

import { environment } from '../enviroment/environment';
// ⬆️ Ajustado a tu ruta real

@Injectable({
  providedIn: 'root'
})
export class PerfilService {

  // URL base + endpoint
  private api = `${environment.apiBaseUrl}/perfil`;

  constructor(private http: HttpClient) {}

  /** GET /perfil/me */
  getMiPerfil(): Observable<PerfilUsuario> {
    return this.http.get<PerfilUsuario>(`${this.api}/me`);
  }

  /** PUT /perfil/me */
  actualizarMiPerfil(payload: FormData): Observable<PerfilUsuario> {
    return this.http.put<PerfilUsuario>(`${this.api}/me`, payload);
  }
}
