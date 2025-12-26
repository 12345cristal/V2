// src/app/service/gemini-ia.service.ts
import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

export interface ChatbotRequest {
  mensaje: string;
  nino_id?: number;
  incluir_contexto?: boolean;
  session_id?: string;
}

export interface ChatbotResponse {
  respuesta: string;
  contexto_usado: boolean;
  configurado: boolean;
  session_id: string;
}

export interface EstadoResponse {
  configurado: boolean;
  model?: string;
}

@Injectable({ providedIn: 'root' })
export class GeminiIaService {
  // 👈 PROXY: No usa http://localhost:8000 directamente
  private readonly baseUrl = '/api/v1/ia';

  constructor(private http: HttpClient) {}

  /**
   * Chatbot: Consulta de IA
   */
  chatbot(payload: ChatbotRequest): Observable<ChatbotResponse> {
    return this.http.post<ChatbotResponse>(`${this.baseUrl}/chatbot`, payload);
  }

  /**
   * Inicia una nueva sesión de chat
   */
  iniciarSesion(): Observable<{ session_id: string }> {
    return this.http.post<{ session_id: string }>(`${this.baseUrl}/chat/sesion`, {});
  }

  /**
   * Verifica el estado de Gemini
   */
  verificarEstado(): Observable<EstadoResponse> {
    return this.http.get<EstadoResponse>(`${this.baseUrl}/estado`);
  }
}
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
