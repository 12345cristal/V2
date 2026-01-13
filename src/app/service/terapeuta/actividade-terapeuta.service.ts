import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../../environment/environment';
import { Actividad } from '../../interfaces/terapeuta/actividad.interface';

@Injectable({ providedIn: 'root' })
export class ActividadesService {

  private readonly api = `${environment.apiBaseUrl}/actividades`;

  constructor(private http: HttpClient) {}

  /**
   * Catálogo general de actividades
   */
  getActividades(): Observable<Actividad[]> {
    return this.http.get<Actividad[]>(this.api);
  }

  /**
   * Crear nueva actividad terapéutica
   */
  crearActividad(data: Partial<Actividad>): Observable<Actividad> {
    return this.http.post<Actividad>(this.api, data);
  }

  /**
   * Asignar actividad a un niño
   * → tabla tareas_recurso
   */
  asignarActividadANino(payload: {
    recurso_id: number;
    nino_id: number;
    fecha_limite?: string;
  }): Observable<any> {
    return this.http.post(
      `${environment.apiBaseUrl}/tareas-recurso`,
      payload
    );
  }

  /**
   * Actividades asignadas a un niño
   */
  getActividadesPorNino(ninoId: number): Observable<any[]> {
    return this.http.get<any[]>(
      `${environment.apiBaseUrl}/ninos/${ninoId}/tareas`
    );
  }

}
