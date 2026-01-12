import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../environments/environment';
import { Terapia, AsignacionTerapia } from '../interfaces/terapia.interfaz';

/**
 * Representa un terapeuta recomendado por el sistema de soporte a la decisión (TOPSIS)
 */
export interface TerapeutaRecomendado {
  id_personal: number;        // ID del terapeuta
  nombre_completo: string;    // Nombre completo
  score: number;              // Puntuación calculada (TOPSIS)
  rank: number;               // Posición en la recomendación
  id_terapia: number;         // Terapia para la que se recomienda
  terapia_nombre: string;     // Nombre de la terapia
  criterios: {                // Valores utilizados para cálculo
    rating: number;
    carga: number;
    sesiones: number;
    afinidad: number;
    [key: string]: any;
  };
}

@Injectable({
  providedIn: 'root'
})
export class TherapyService {

  private api = `${environment.apiBaseUrl}/terapias`;

  constructor(private http: HttpClient) {}

  // ============================
  // 📌 CRUD de terapias
  // ============================

  getTerapias(): Observable<Terapia[]> {
    return this.http.get<Terapia[]>(this.api);
  }

  crearTerapia(data: Terapia): Observable<Terapia> {
    return this.http.post<Terapia>(this.api, data);
  }

  actualizarTerapia(id: number, data: Terapia): Observable<Terapia> {
    return this.http.put<Terapia>(`${this.api}/${id}`, data);
  }

  cambiarEstado(id: number): Observable<Terapia> {
    return this.http.patch<Terapia>(`${this.api}/${id}/estado`, {});
  }

  // ============================
  // 📌 Personal asignado y disponible
  // ============================

  getPersonalDisponible(): Observable<any> {
    return this.http.get(`${environment.apiBaseUrl}/personal/sin-terapia`);
  }

  getPersonalAsignado(): Observable<any> {
    return this.http.get(`${this.api}/personal-asignado`);
  }

  asignarPersonal(data: AsignacionTerapia): Observable<any> {
    return this.http.post(`${this.api}/asignar`, data);
  }

  asignarTerapia(id_personal: number, id_terapia: number): Observable<any> {
    return this.http.post(`${this.api}/asignar`, { id_personal, id_terapia });
  }

  // ============================
  // 📌 Recomendación de terapeutas (TOPSIS / Decision Support)
  // ============================

  /**
   * Obtiene los terapeutas recomendados para una terapia específica.
   * El payload puede incluir criterios de filtrado como:
   * - id_terapia
   * - disponibilidad
   * - afinidad clínica
   * - carga laboral máxima
   * ✅ Actualizado para usar endpoint correcto
   */
  recomendarTerapeutas(payload: any): Observable<TerapeutaRecomendado[]> {
    // ✅ Usar el endpoint correcto de TOPSIS
    return this.http.post<TerapeutaRecomendado[]>(
      `${environment.apiBaseUrl}/topsis/prioridad-ninos`,
      payload
    );
  }
}
