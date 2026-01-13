// src/app/service/planes-pago.service.ts
import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from 'src/environments/environment';
import {
  PlanPago,
  PlanPagoListItem,
  PlanPagoCreate,
  PlanPagoUpdate,
  SaldoPendiente
} from '../interfaces/plan-pago.interface';

@Injectable({
  providedIn: 'root'
})
export class PlanesPagoService {
  private apiUrl = `${environment.apiBaseUrl}/planes-pago`;

  constructor(private http: HttpClient) {}

  listar(filtros?: {
    ninoId?: number;
    activo?: number;
    estado?: string;
    skip?: number;
    limit?: number;
  }): Observable<PlanPagoListItem[]> {
    let params = new HttpParams();
    if (filtros) {
      if (filtros.ninoId) params = params.set('nino_id', filtros.ninoId.toString());
      if (filtros.activo !== undefined) params = params.set('activo', filtros.activo.toString());
      if (filtros.estado) params = params.set('estado', filtros.estado);
      if (filtros.skip) params = params.set('skip', filtros.skip.toString());
      if (filtros.limit) params = params.set('limit', filtros.limit.toString());
    }
    return this.http.get<PlanPagoListItem[]>(this.apiUrl, { params });
  }

  listarPorNino(ninoId: number, activo?: number): Observable<PlanPagoListItem[]> {
    let params = new HttpParams();
    if (activo !== undefined) {
      params = params.set('activo', activo.toString());
    }
    return this.http.get<PlanPagoListItem[]>(`${this.apiUrl}/nino/${ninoId}`, { params });
  }

  obtener(planId: number): Observable<PlanPago> {
    return this.http.get<PlanPago>(`${this.apiUrl}/${planId}`);
  }

  crear(plan: PlanPagoCreate): Observable<PlanPago> {
    return this.http.post<PlanPago>(this.apiUrl, plan);
  }

  actualizar(planId: number, plan: PlanPagoUpdate): Observable<PlanPago> {
    return this.http.put<PlanPago>(`${this.apiUrl}/${planId}`, plan);
  }

  eliminar(planId: number): Observable<void> {
    return this.http.delete<void>(`${this.apiUrl}/${planId}`);
  }

  calcularSaldo(planId: number): Observable<SaldoPendiente> {
    return this.http.get<SaldoPendiente>(`${this.apiUrl}/${planId}/saldo`);
  }

  recalcular(planId: number): Observable<PlanPago> {
    return this.http.post<PlanPago>(`${this.apiUrl}/${planId}/recalcular`, {});
  }
}

