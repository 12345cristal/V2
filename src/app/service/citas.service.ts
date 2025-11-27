import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';

import { environment } from '../enviroment/environment';

import {
  CitaListado,
  CatalogosCitaResponse,
  EstadoCitaOpcion,
  NinoResumen,
  TerapiaBasica,
  EstadoCita,
  CrearCitaDto
} from '../coordinador/interfaces/cita.interface';

@Injectable({
  providedIn: 'root'
})
export class CitasService {

  private apiUrl = `${environment.apiBaseUrl}/citas`;

  constructor(private http: HttpClient) {}

  obtenerCatalogos(): Observable<CatalogosCitaResponse> {
    return this.http.get<CatalogosCitaResponse>(`${this.apiUrl}/catalogos`);
  }

  obtenerCitas(
    fecha?: string | null,
    estado?: EstadoCita | null,
    ninoId?: number | null
  ): Observable<CitaListado[]> {

    let params = new HttpParams();

    if (fecha) params = params.set('fecha', fecha);
    if (estado) params = params.set('estado', estado);
    if (ninoId) params = params.set('ninoId', String(ninoId));

    return this.http.get<CitaListado[]>(this.apiUrl, { params });
  }

  crearCita(payload: CrearCitaDto): Observable<CitaListado> {
    return this.http.post<CitaListado>(this.apiUrl, payload);
  }

  actualizarCita(id: number, payload: any): Observable<CitaListado> {
    return this.http.put<CitaListado>(`${this.apiUrl}/${id}`, payload);
  }

  cancelarCita(id: number, motivoCancelacion: string): Observable<CitaListado> {
    return this.http.patch<CitaListado>(`${this.apiUrl}/${id}/cancelar`, {
      motivoCancelacion
    });
  }

  reprogramarCita(id: number, payload: any): Observable<CitaListado> {
    return this.http.patch<CitaListado>(`${this.apiUrl}/${id}/reprogramar`, payload);
  }
}
