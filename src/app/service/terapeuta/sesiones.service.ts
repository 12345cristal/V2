import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../../environment/environment';
import { Sesion } from '../../interfaces/terapeuta/sesion.interface';

export type CrearSesionPayload = {
  terapia_nino_id: number;
  fecha: string; // ISO datetime
  asistio: boolean;
  progreso?: number | null;
  colaboracion?: number | null;
  observaciones?: string | null;
};

export type ActualizarSesionPayload = Partial<Omit<Sesion, 'id'>>;

@Injectable({ providedIn: 'root' })
export class SesionesService {
  private readonly api = `${environment.apiBaseUrl}/terapeuta/sesiones`;

  constructor(private http: HttpClient) {}

  /**
   * Listar sesiones por niño
   * Backend recomendado: filtra por terapeuta autenticado
   */
  getSesionesPorNino(ninoId: number): Observable<Sesion[]> {
    return this.http.get<Sesion[]>(`${this.api}/nino/${ninoId}`);
  }

  /**
   * (Opcional) listar por terapia_nino_id si quieres vista por terapia específica
   */
  getSesionesPorTerapiaNino(terapiaNinoId: number): Observable<Sesion[]> {
    return this.http.get<Sesion[]>(`${this.api}/terapia-nino/${terapiaNinoId}`);
  }

  /**
   * Crear sesión (cuando termina una terapia o para registrar en el momento)
   */
  crearSesion(payload: CrearSesionPayload): Observable<Sesion> {
    return this.http.post<Sesion>(this.api, payload);
  }

  /**
   * Actualizar sesión (editar observaciones/asistencia)
   */
  actualizarSesion(sesionId: number, payload: ActualizarSesionPayload) {
    return this.http.patch(`${this.api}/${sesionId}`, payload);
  }
}
