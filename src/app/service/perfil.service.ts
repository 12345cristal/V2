import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { map } from 'rxjs/operators';
import { PerfilUsuario } from '../interfaces/perfil-usuario.interface';

import { environment } from '../enviroment/environment';

@Injectable({
  providedIn: 'root'
})
export class PerfilService {

  private api = `${environment.apiBaseUrl}/perfil`;

  constructor(private http: HttpClient) {}

  /** GET /perfil/me */
  getMiPerfil(): Observable<PerfilUsuario> {
    return this.http.get<PerfilUsuario>(`${this.api}/me`).pipe(
      map(data => this.construirUrlsArchivos(data))
    );
  }

  /** PUT /perfil/me */
  actualizarMiPerfil(payload: FormData): Observable<PerfilUsuario> {
    return this.http.put<PerfilUsuario>(`${this.api}/me`, payload).pipe(
      map(data => this.construirUrlsArchivos(data))
    );
  }

  private construirUrlsArchivos(data: PerfilUsuario): PerfilUsuario {
    if (data.foto_perfil && !data.foto_perfil.startsWith('http')) {
      const parts = data.foto_perfil.split('/');
      const tipo = parts[0];
      const filename = parts[1];
      data.foto_perfil = `${this.api}/archivos/${tipo}/${filename}`;
    }

    if (data.cv_archivo && !data.cv_archivo.startsWith('http')) {
      const parts = data.cv_archivo.split('/');
      const tipo = parts[0];
      const filename = parts[1];
      data.cv_archivo = `${this.api}/archivos/${tipo}/${filename}`;
    }

    if (data.documentos_extra && data.documentos_extra.length > 0) {
      data.documentos_extra = data.documentos_extra.map(url => {
        if (!url.startsWith('http')) {
          const parts = url.split('/');
          const tipo = parts[0];
          const filename = parts[1];
          return `${this.api}/archivos/${tipo}/${filename}`;
        }
        return url;
      });
    }

    return data;
  }
}
