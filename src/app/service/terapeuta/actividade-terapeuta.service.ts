import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { Actividad } from '../../interfaces/terapeuta/actividad.interface';
import { ActividadAsignada } from '../../interfaces/terapeuta/actividad-asignada.interface';
import { environment } from '../../environment/environment';

@Injectable({ providedIn: 'root' })
export class ActividadesService {
  private base = `${environment.apiBaseUrl}/actividades`;

  constructor(private http: HttpClient) {}

  listar(): Observable<Actividad[]> {
    return this.http.get<Actividad[]>(this.base);
  }

  crear(data: FormData): Observable<Actividad> {
    return this.http.post<Actividad>(this.base, data);
  }

  getActividadesPorTerapeuta(): Observable<ActividadAsignada[]> {
    return this.http.get<ActividadAsignada[]>(`${this.base}/terapeuta`);
  }
}
