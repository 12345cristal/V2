import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment    } from '../../environment/environment';
import { Sesion } from '../../interfaces/terapeuta/sesion.interface';

@Injectable({ providedIn: 'root' })
export class AsistenciasService {

  private readonly api = `${environment.apiBaseUrl}/terapeuta/sesiones`;

  constructor(private http: HttpClient) {}

  /**
   * Sesiones del terapeuta (por semana o rango)
   */
  getSesiones(params?: {
    desde?: string;
    hasta?: string;
  }): Observable<Sesion[]> {
    return this.http.get<Sesion[]>(this.api, { params });
  }

  /**
   * Registrar asistencia de una sesión
   */
  registrarAsistencia(payload: {
    sesion_id: number;
    asistio: boolean;
    observaciones?: string;
    progreso?: number;
    colaboracion?: number;
  }): Observable<any> {
    return this.http.post(`${this.api}/asistencia`, payload);
  }

}
