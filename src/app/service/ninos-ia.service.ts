// src/app/service/ninos-ia.service.ts
import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { environment } from '../environments/environment';
import { Observable } from 'rxjs';

export interface NinoIAAnalisisResponse {
  metricas: any;
  perfil_textual: string;
  analisis_emocional: string;
  recomendaciones_terapias: string;
  recomendaciones_actividades: string;
  explicacion_para_padres: string;
}

@Injectable({ providedIn: 'root' })
export class NinosIAService {

  private baseUrl = `${environment.apiBaseUrl}/ia/ninos`;

  constructor(private http: HttpClient) {}

  analizarNino(ninoId: number, textoExtra?: string): Observable<NinoIAAnalisisResponse> {
    return this.http.post<NinoIAAnalisisResponse>(
      `${this.baseUrl}/${ninoId}/analisis-completo`,
      { texto_extra: textoExtra ?? null }
    );
  }
}
