import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

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

  private baseUrl = 'http://localhost:8000/api/v1/decision-support';

  constructor(private http: HttpClient) {}

  calcularPrioridad(payload: any): Observable<NinoPrioritario[]> {
    return this.http.post<NinoPrioritario[]>(`${this.baseUrl}/prioridad-ninos`, payload);
  }

  descargarPdfPrioridad(payload: any): Observable<Blob> {
    return this.http.post(`${this.baseUrl}/prioridad-ninos/pdf`, payload, {
      responseType: 'blob'
    });
  }
}
