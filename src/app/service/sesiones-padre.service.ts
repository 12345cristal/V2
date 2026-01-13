import { Injectable, inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from 'src/environments/environment';
import { Sesion, SesionDetalle } from '../interfaces/sesiones.interface';

@Injectable({ providedIn: 'root' })
export class SesionesPadreService {
  private http = inject(HttpClient);
  private baseUrl = `${environment.apiBaseUrl}/padre/sesiones`;

  getHoy(hijoId: number): Observable<Sesion[]> {
    return this.http.get<Sesion[]>(`${this.baseUrl}/hoy/${hijoId}`);
  }

  getProgramadas(hijoId: number): Observable<Sesion[]> {
    return this.http.get<Sesion[]>(`${this.baseUrl}/programadas/${hijoId}`);
  }

  getSemana(hijoId: number): Observable<Sesion[]> {
    return this.http.get<Sesion[]>(`${this.baseUrl}/semana/${hijoId}`);
  }

  getDetalle(id: number): Observable<SesionDetalle> {
    return this.http.get<SesionDetalle>(`${this.baseUrl}/${id}`);
  }

  descargarBitacora(id: number): Observable<Blob> {
    return this.http.get(`${this.baseUrl}/${id}/bitacora`, {
      responseType: 'blob'
    });
  }
}

