import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../../environments/environment';

export interface NinoPrioritario {
  id: number;
  rank: number;
  nombre_completo: string;
  score: number;
  criterios: {
    prioridad: number;
    dias_sin_sesion: number;
    asistencias: number;
    inasistencias: number;
  };
}

@Injectable({
  providedIn: 'root'
})
export class DecisionSupportService {

  // ✅ Actualizado para usar endpoint correcto de TOPSIS
  private baseUrl = `${environment.apiBaseUrl}/topsis`;

  constructor(private http: HttpClient) {}

  calcularPrioridad(payload: any): Observable<NinoPrioritario[]> {
    // ✅ Usa el endpoint correcto: /topsis/prioridad-ninos
    return this.http.post<NinoPrioritario[]>(`${this.baseUrl}/prioridad-ninos`, payload);
  }

  descargarPdfPrioridad(payload: any): Observable<Blob> {
    // ✅ Este endpoint puede no existir aún, mantenerlo por compatibilidad
    return this.http.post(`${this.baseUrl}/prioridad-ninos/pdf`, payload, {
      responseType: 'blob'
    });
  }
}




