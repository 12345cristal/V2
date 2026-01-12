// src/app/service/terapias-nino.service.ts

import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';

import {
  NinoTerapiasDetalle,
  TerapiaAsignadaNino,
  TerapiaNino,
  TerapiaNinoCreate,
  TerapiaNinoUpdate
} from '../interfaces/terapias-nino.interface';

import { environment } from '../enviroment/environment';

@Injectable({
  providedIn: 'root'
})
export class TerapiasNinoService {

  private readonly baseUrl = environment.apiBaseUrl;
  private readonly apiUrl = `${this.baseUrl}/terapias-nino`;

  constructor(private http: HttpClient) {}

  // ==================== MÉTODOS LEGACY (para compatibilidad) ====================

  /**
   * Obtiene el resumen del niño + terapias asignadas.
   * GET /ninos/{id}/terapias
   */
  obtenerTerapiasDeNino(idNino: number): Observable<NinoTerapiasDetalle> {
    return this.http.get<NinoTerapiasDetalle>(
      `${this.baseUrl}/ninos/${idNino}/terapias`
    );
  }

  /**
   * Solo listado de terapias asignadas al niño.
   * GET /ninos/{id}/terapias/listado
   */
  obtenerSoloTerapiasDeNino(idNino: number): Observable<TerapiaAsignadaNino[]> {
    return this.http.get<TerapiaAsignadaNino[]>(
      `${this.baseUrl}/ninos/${idNino}/terapias/listado`
    );
  }

  // ==================== NUEVOS MÉTODOS (estructura real BD) ====================

  listarPorNino(ninoId: number, activo?: number): Observable<TerapiaNino[]> {
    let params = new HttpParams();
    if (activo !== undefined) {
      params = params.set('activo', activo.toString());
    }
    return this.http.get<TerapiaNino[]>(`${this.apiUrl}/nino/${ninoId}`, { params });
  }

  listarActivasPorNino(ninoId: number): Observable<TerapiaNino[]> {
    return this.http.get<TerapiaNino[]>(`${this.apiUrl}/activas/nino/${ninoId}`);
  }

  listarPorTerapeuta(terapeutaId: number, activo: number = 1): Observable<TerapiaNino[]> {
    const params = new HttpParams().set('activo', activo.toString());
    return this.http.get<TerapiaNino[]>(`${this.apiUrl}/terapeuta/${terapeutaId}/ninos`, { params });
  }

  obtener(terapiaNinoId: number): Observable<TerapiaNino> {
    return this.http.get<TerapiaNino>(`${this.apiUrl}/${terapiaNinoId}`);
  }

  asignar(terapia: TerapiaNinoCreate): Observable<TerapiaNino> {
    return this.http.post<TerapiaNino>(this.apiUrl, terapia);
  }

  actualizar(terapiaNinoId: number, terapia: TerapiaNinoUpdate): Observable<TerapiaNino> {
    return this.http.put<TerapiaNino>(`${this.apiUrl}/${terapiaNinoId}`, terapia);
  }

  desactivar(terapiaNinoId: number): Observable<void> {
    return this.http.delete<void>(`${this.apiUrl}/${terapiaNinoId}`);
  }

  reactivar(terapiaNinoId: number): Observable<TerapiaNino> {
    return this.http.post<TerapiaNino>(`${this.apiUrl}/${terapiaNinoId}/reactivar`, {});
  }
}
