// src/app/service/recomendaciones-actividades.service.ts
import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../environment/environment';

export interface ActividadRecomendada {
  actividad_id: number;
  nombre: string;
  descripcion: string | null;
  area_desarrollo: string | null;
  dificultad: number;
  duracion_minutos: number;
  score_similitud: number;
  ranking: number;
  razon_recomendacion: string;
  tags: string[];
}

export interface RecomendacionResponse {
  nino_id: number;
  nombre_nino: string;
  total_recomendaciones: number;
  perfil_actualizado: boolean;
  fecha_generacion: string;
  recomendaciones: ActividadRecomendada[];
}

export interface RecomendacionRequest {
  nino_id: number;
  top_n?: number;
  actualizar_perfil?: boolean;
  filtrar_por_area?: string | null;
  nivel_dificultad_max?: number | null;
}

export interface PerfilNino {
  nino_id: number;
  nombre_nino: string;
  edad: number | null;
  diagnosticos: string[];
  dificultades: string[];
  fortalezas: string[];
  areas_prioritarias: string[];
  fecha_ultima_actualizacion: string | null;
  tiene_embedding: boolean;
}

export interface ProgresoRequest {
  nino_id: number;
  actividad_id: number;
  terapeuta_id: number;
  calificacion: number;
  notas_progreso?: string | null;
  dificultad_encontrada?: number | null;
}

@Injectable({
  providedIn: 'root'
})
export class RecomendacionesActividadesService {
  private apiUrl = `${environment.apiBaseUrl}/recomendaciones-actividades`;

  constructor(private http: HttpClient) {}

  /**
   * Genera recomendaciones personalizadas de actividades
   */
  generarRecomendaciones(request: RecomendacionRequest): Observable<RecomendacionResponse> {
    return this.http.post<RecomendacionResponse>(`${this.apiUrl}/generar`, request);
  }

  /**
   * Obtiene recomendaciones rápidas (5 actividades)
   */
  obtenerRecomendacionesRapidas(ninoId: number): Observable<RecomendacionResponse> {
    return this.http.get<RecomendacionResponse>(`${this.apiUrl}/quick/${ninoId}`);
  }

  /**
   * Obtiene el perfil de un niño
   */
  obtenerPerfilNino(ninoId: number): Observable<PerfilNino> {
    return this.http.get<PerfilNino>(`${this.apiUrl}/perfil/${ninoId}`);
  }

  /**
   * Registra el progreso en una actividad
   */
  registrarProgreso(request: ProgresoRequest): Observable<any> {
    return this.http.post(`${this.apiUrl}/progreso`, request);
  }
}
