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

  /** Descargar archivo como Blob (para obtener contenido completo) */
  descargarArchivo(urlCompleta: string): Observable<Blob> {
    return this.http.get(urlCompleta, {
      responseType: 'blob'
    });
  }

  /** Alias: Descargar archivo protegido con JWT como Blob */
  descargarArchivoProtegido(urlCompleta: string): Observable<Blob> {
    return this.descargarArchivo(urlCompleta);
  }

  private construirUrlsArchivos(data: PerfilUsuario): PerfilUsuario {
    if (data.foto_perfil && !data.foto_perfil.startsWith('http')) {
      const filename = data.foto_perfil.split('/').pop() || data.foto_perfil;
      data.foto_perfil = `${this.api}/archivos/fotos/${filename}`;
    }

    if (data.cv_archivo && !data.cv_archivo.startsWith('http')) {
      const filename = data.cv_archivo.split('/').pop() || data.cv_archivo;
      data.cv_archivo = `${this.api}/archivos/cv/${filename}`;
    }

    if (data.documentos_extra && data.documentos_extra.length > 0) {
      data.documentos_extra = data.documentos_extra.map(url => {
        if (!url.startsWith('http')) {
          const filename = url.split('/').pop() || url;
          return `${this.api}/archivos/documentos/${filename}`;
        }
        return url;
      });
    }

    return data;
  }
}

