import { Injectable, inject } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({ providedIn: 'root' })
export class ArchivosService {
  private http = inject(HttpClient);

  /**
   * Descarga un archivo protegido. El token se puede:
   * - agregar por interceptor (recomendado), o
   * - pasar explícitamente aquí (opcional).
   */
  descargarComoBlob(url: string, token?: string): Observable<Blob> {
    const headers = token
      ? new HttpHeaders({ Authorization: `Bearer ${token}` })
      : undefined;

    return this.http.get(url, {
      responseType: 'blob',
      headers,
      // withCredentials: true, // Actívalo si tu auth es por cookies
    });
  }
}
