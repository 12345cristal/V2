// src/app/service/gemini-ia.service.ts
import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

export interface ChatbotRequest {
  mensaje: string;
  nino_id?: number;
  incluir_contexto?: boolean;
}

export interface ChatbotResponse {
  respuesta: string;
  contexto_usado: boolean;
  configurado: boolean;
}

export interface ActividadGenerada {
  nombre: string;
  descripcion: string;
  objetivo: string;
  duracion_minutos: number;
  materiales: string[];
  nivel_dificultad: string;
  area_desarrollo: string;
}

export interface PlanTerapeutico {
  objetivos_generales: string[];
  areas_enfoque: string[];
  frecuencia_sesiones: string;
  terapias_recomendadas: Array<{tipo: string; justificacion: string}>;
  indicadores_progreso: string[];
  recomendaciones_padres: string[];
}

export interface AnalisisProgreso {
  resumen: string;
  areas_mejora: string[];
  areas_oportunidad: string[];
  tendencias: string[];
  recomendaciones_ajuste: string[];
  proximos_objetivos: string[];
  calificacion_progreso: number;
}

@Injectable({
  providedIn: 'root'
})
export class GeminiIaService {
  private baseUrl = 'http://localhost:8000/api/v1/ia';

  constructor(private http: HttpClient) {}

  /**
   * Chatbot de consultas sobre autismo
   */
  chatbot(request: ChatbotRequest): Observable<ChatbotResponse> {
    return this.http.post<ChatbotResponse>(`${this.baseUrl}/chatbot`, request);
  }

  /**
   * Generar actividades personalizadas
   */
  generarActividades(ninoId: number, cantidad: number = 5, objetivos?: string): Observable<ActividadGenerada[]> {
    return this.http.post<ActividadGenerada[]>(`${this.baseUrl}/actividades-personalizadas`, {
      nino_id: ninoId,
      cantidad: cantidad,
      objetivos_especificos: objetivos
    });
  }

  /**
   * Generar plan terapéutico
   */
  generarPlanTerapeutico(ninoId: number, evaluacion: string, objetivosPadres?: string): Observable<PlanTerapeutico> {
    return this.http.post<PlanTerapeutico>(`${this.baseUrl}/plan-terapeutico`, {
      nino_id: ninoId,
      evaluacion_inicial: evaluacion,
      objetivos_padres: objetivosPadres
    });
  }

  /**
   * Analizar progreso
   */
  analizarProgreso(ninoId: number, evaluaciones: any[], periodo: string = 'últimos 3 meses'): Observable<AnalisisProgreso> {
    return this.http.post<AnalisisProgreso>(`${this.baseUrl}/analizar-progreso`, {
      nino_id: ninoId,
      evaluaciones: evaluaciones,
      periodo: periodo
    });
  }

  /**
   * Verificar estado de Gemini
   */
  verificarEstado(): Observable<any> {
    return this.http.get(`${this.baseUrl}/estado`);
  }
}
