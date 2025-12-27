import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, catchError, throwError } from 'rxjs';

export interface EstadoGeminiResponse {
  configurado: boolean;
  model?: string;
}

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

@Injectable({ providedIn: 'root' })
export class GeminiIaService {
  // URL absoluta al backend (no proxy)
  private readonly baseUrl = 'http://localhost:8000/api/v1/ia';

  constructor(private http: HttpClient) {}

  verificarEstado(): Observable<EstadoGeminiResponse> {
    return this.http.get<EstadoGeminiResponse>(`${this.baseUrl}/estado`).pipe(
      catchError((err) => {
        return throwError(() => ({
          message: 'No se pudo verificar el estado del servicio IA.',
          detail: err?.error?.detail ?? 'Error de conexión o servidor',
          status: err?.status ?? 0,
        }));
      })
    );
  }

  iniciarSesion(): Observable<{ session_id: string }> {
    return this.http.post<{ session_id: string }>(`${this.baseUrl}/chat/sesion`, {}).pipe(
      catchError((err) => {
        return throwError(() => ({
          message: 'No se pudo iniciar la sesión de chat.',
          detail: err?.error?.detail ?? 'Error de conexión o servidor',
          status: err?.status ?? 0,
        }));
      })
    );
  }

  chatbot(payload: ChatbotRequest): Observable<ChatbotResponse> {
    return this.http.post<ChatbotResponse>(`${this.baseUrl}/chatbot`, payload).pipe(
      catchError((err) => {
        return throwError(() => ({
          message: 'El chatbot no pudo procesar tu solicitud.',
          detail: err?.error?.detail ?? 'Error de conexión o servidor',
          status: err?.status ?? 0,
        }));
      })
    );
  }
}
