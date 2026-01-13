// src/app/service/pagos.service.ts
import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../../environments/environment';
import {
  Pago,
  PagoListItem,
  PagoCreate,
  PagoUpdate,
  HistorialPagos
} from '../interfaces/pago.interface';

@Injectable({
  providedIn: 'root'
})
export class PagosService {
  private apiUrl = `${environment.apiBaseUrl}/pagos`;

  constructor(private http: HttpClient) {}

  listar(filtros?: {
    planId?: number;
    usuarioId?: number;
    estado?: string;
    skip?: number;
    limit?: number;
  }): Observable<PagoListItem[]> {
    let params = new HttpParams();
    if (filtros) {
      if (filtros.planId) params = params.set('plan_id', filtros.planId.toString());
      if (filtros.usuarioId) params = params.set('usuario_id', filtros.usuarioId.toString());
      if (filtros.estado) params = params.set('estado', filtros.estado);
      if (filtros.skip) params = params.set('skip', filtros.skip.toString());
      if (filtros.limit) params = params.set('limit', filtros.limit.toString());
    }
    return this.http.get<PagoListItem[]>(this.apiUrl, { params });
  }

  listarPorPlan(planId: number, estado?: string): Observable<PagoListItem[]> {
    let params = new HttpParams();
    if (estado) {
      params = params.set('estado', estado);
    }
    return this.http.get<PagoListItem[]>(`${this.apiUrl}/plan/${planId}`, { params });
  }

  obtener(pagoId: number): Observable<Pago> {
    return this.http.get<Pago>(`${this.apiUrl}/${pagoId}`);
  }

  registrar(pago: PagoCreate): Observable<Pago> {
    return this.http.post<Pago>(this.apiUrl, pago);
  }

  actualizar(pagoId: number, pago: PagoUpdate): Observable<Pago> {
    return this.http.put<Pago>(`${this.apiUrl}/${pagoId}`, pago);
  }

  eliminar(pagoId: number): Observable<void> {
    return this.http.delete<void>(`${this.apiUrl}/${pagoId}`);
  }

  obtenerHistorialUsuario(usuarioId: number, limite: number = 50): Observable<HistorialPagos> {
    const params = new HttpParams().set('limite', limite.toString());
    return this.http.get<HistorialPagos>(`${this.apiUrl}/usuario/${usuarioId}/historial`, { params });
  }
}




