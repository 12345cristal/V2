import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';

import { environment } from 'src/environments/environment';

import {
  Cita,
  CitaCreate,
  CitaUpdate,
  CitaListResponse,
  EstadoCitaCatalogo,
  CitaFiltros
} from '../interfaces/cita.interface';

@Injectable({
  providedIn: 'root'
})
export class CitasService {

  private apiUrl = `${environment.apiBaseUrl}/citas`;

  constructor(private http: HttpClient) {}

  /**
   * Obtener lista de citas con filtros y paginación
   */
  getCitas(filtros: CitaFiltros = {}): Observable<CitaListResponse> {
    let params = new HttpParams();
    
    if (filtros.fecha) params = params.set('fecha', filtros.fecha);
    if (filtros.nino_id) params = params.set('nino_id', filtros.nino_id.toString());
    if (filtros.terapeuta_id) params = params.set('terapeuta_id', filtros.terapeuta_id.toString());
    if (filtros.terapia_id) params = params.set('terapia_id', filtros.terapia_id.toString());
    if (filtros.estado_id) params = params.set('estado_id', filtros.estado_id.toString());
    if (filtros.buscar) params = params.set('buscar', filtros.buscar);
    if (filtros.page) params = params.set('page', filtros.page.toString());
    if (filtros.page_size) params = params.set('page_size', filtros.page_size.toString());

    return this.http.get<CitaListResponse>(this.apiUrl, { params });
  }

  /**
   * Obtener una cita por ID
   */
  getCitaById(id: number): Observable<Cita> {
    return this.http.get<Cita>(`${this.apiUrl}/${id}`);
  }

  /**
   * Crear una nueva cita
   */
  createCita(cita: CitaCreate): Observable<Cita> {
    return this.http.post<Cita>(this.apiUrl, cita);
  }

  /**
   * Actualizar una cita existente
   */
  updateCita(id: number, cita: CitaUpdate): Observable<Cita> {
    return this.http.put<Cita>(`${this.apiUrl}/${id}`, cita);
  }

  /**
   * Cambiar el estado de una cita
   */
  cambiarEstado(id: number, estadoId: number): Observable<Cita> {
    return this.http.patch<Cita>(`${this.apiUrl}/${id}/estado`, null, {
      params: { estado_id: estadoId.toString() }
    });
  }

  /**
   * Eliminar una cita
   */
  deleteCita(id: number): Observable<{ message: string }> {
    return this.http.delete<{ message: string }>(`${this.apiUrl}/${id}`);
  }

  /**
   * Obtener catálogo de estados de cita
   */
  getEstadosCita(): Observable<EstadoCitaCatalogo[]> {
    return this.http.get<EstadoCitaCatalogo[]>(`${environment.apiBaseUrl}/estados-cita`);
  }
}

