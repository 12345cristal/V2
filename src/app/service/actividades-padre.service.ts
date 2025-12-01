import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { environment } from '../enviroment/environment';

import {
  ActividadAsignadaPadre,
  CompletarActividadPadreDto,
  CrearValoracionPadreDto,
  ResumenActividadesPadre
} from '../interfaces/actividades-padre.interface';

@Injectable({
  providedIn: 'root'
})
export class ActividadesPadreService {

  private baseUrl = `${environment.apiBaseUrl}/padre/actividades`;

  constructor(private http: HttpClient) {}

  // Todas las actividades asignadas a los hijos de este padre
  getMisActividades() {
    return this.http.get<ActividadAsignadaPadre[]>(`${this.baseUrl}`);
  }

  // Una sola asignación (detalle)
  getActividadAsignada(id: number) {
    return this.http.get<ActividadAsignadaPadre>(`${this.baseUrl}/${id}`);
  }

  // Marcar completada + comentarios
  completarActividad(id: number, dto: CompletarActividadPadreDto) {
    return this.http.post<ActividadAsignadaPadre>(`${this.baseUrl}/${id}/completar`, dto);
  }

  // Enviar valoración
  valorarActividad(id: number, dto: CrearValoracionPadreDto) {
    return this.http.post<ActividadAsignadaPadre>(`${this.baseUrl}/${id}/valorar`, dto);
  }

  // (Opcional) Resumen desde backend
  getResumen() {
    return this.http.get<ResumenActividadesPadre>(`${this.baseUrl}/resumen`);
  }
}
