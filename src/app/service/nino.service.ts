// src/app/service/nino.service.ts
import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../enviroment/environment';
import { Nino } from '../interfaces/nino.interface';

@Injectable({
  providedIn: 'root'
})
export class NinosService {

  private baseUrl = `${environment.apiBaseUrl}/ninos`;

  constructor(private http: HttpClient) {}

  // ==================== CRUD BÁSICO ====================

  listar(filtros?: {
    tutorId?: number;
    estado?: string;
    busqueda?: string;
    skip?: number;
    limit?: number;
  }): Observable<any[]> {
    let params = new HttpParams();
    if (filtros) {
      if (filtros.tutorId) params = params.set('tutor_id', filtros.tutorId.toString());
      if (filtros.estado) params = params.set('estado', filtros.estado);
      if (filtros.busqueda) params = params.set('busqueda', filtros.busqueda);
      if (filtros.skip) params = params.set('skip', filtros.skip.toString());
      if (filtros.limit) params = params.set('limit', filtros.limit.toString());
    }
    return this.http.get<any[]>(this.baseUrl, { params });
  }

  listarPorTutor(tutorId: number, estado?: string): Observable<any[]> {
    let params = new HttpParams();
    if (estado) {
      params = params.set('estado', estado);
    }
    return this.http.get<any[]>(`${this.baseUrl}/tutor/${tutorId}`, { params });
  }

  obtenerNinoPorId(id: number): Observable<Nino> {
    return this.http.get<Nino>(`${this.baseUrl}/${id}`);
  }

  crear(nino: any): Observable<Nino> {
    return this.http.post<Nino>(this.baseUrl, nino);
  }

  actualizarNino(id: number, cambios: Partial<Nino>): Observable<Nino> {
    return this.http.put<Nino>(`${this.baseUrl}/${id}`, cambios);
  }

  eliminar(id: number): Observable<void> {
    return this.http.delete<void>(`${this.baseUrl}/${id}`);
  }
}
