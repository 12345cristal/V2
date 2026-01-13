import { Injectable, inject } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { environment } from '../../environments/environment';
import { Observable } from 'rxjs';
import { 
  RecomendacionActividad, 
  RecomendacionTerapia 
} from '../interfaces/recomendacion.interface';

export interface RecursoRecomendado {
  id: number;
  titulo: string;
  descripcion?: string;
  score: number;
}

/**
 * Servicio para recomendaciones basadas en contenido
 * Permite obtener recomendaciones de actividades y terapias para niños
 */
@Injectable({ providedIn: 'root' })
export class RecomendacionService {
  private http = inject(HttpClient);
  private readonly API_URL = `${environment.apiBaseUrl}/recomendacion`;
  private readonly API_PADRES = `${environment.apiBaseUrl}/padres`;

  // ============================================================
  // MÉTODOS PARA RECOMENDACIONES DE ACTIVIDADES Y TERAPIAS
  // ============================================================

  /**
   * Obtiene recomendaciones de actividades para un niño
   * @param ninoId ID del niño
   * @param topN Número de recomendaciones (por defecto 10)
   */
  getRecomendacionActividades(
    ninoId: number, 
    topN: number = 10
  ): Observable<RecomendacionActividad[]> {
    const params = new HttpParams().set('top_n', topN.toString());
    return this.http.get<RecomendacionActividad[]>(
      `${this.API_URL}/actividades/${ninoId}`,
      { params }
    );
  }

  /**
   * Obtiene recomendaciones de terapias para un niño
   * @param ninoId ID del niño
   * @param topN Número de recomendaciones (por defecto 10)
   */
  getRecomendacionTerapias(
    ninoId: number, 
    topN: number = 10
  ): Observable<RecomendacionTerapia[]> {
    const params = new HttpParams().set('top_n', topN.toString());
    return this.http.get<RecomendacionTerapia[]>(
      `${this.API_URL}/terapias/${ninoId}`,
      { params }
    );
  }

  // ============================================================
  // SISTEMA INTELIGENTE DE RECOMENDACIONES (Contenido + TOPSIS + Gemini)
  // ============================================================

  private readonly API_RECOMENDACIONES = `${environment.apiBaseUrl}/recomendaciones`;

  /**
   * Obtiene recomendaciones inteligentes de actividades con explicación de Gemini
   */
  getRecomendacionesInteligentes(
    ninoId: number,
    topN: number = 5,
    incluirExplicacion: boolean = true
  ): Observable<any> {
    const params = new HttpParams()
      .set('top_n', topN.toString())
      .set('incluir_explicacion', incluirExplicacion.toString());
    
    return this.http.post<any>(
      `${this.API_RECOMENDACIONES}/actividades/${ninoId}`,
      null,
      { params }
    );
  }

  /**
   * Selecciona el terapeuta óptimo usando TOPSIS
   */
  seleccionarTerapeutaOptimo(
    ninoId: number,
    terapiaTipo: string,
    criteriosPesos?: any
  ): Observable<any> {
    return this.http.post<any>(
      `${this.API_RECOMENDACIONES}/terapeuta/${ninoId}`,
      {
        terapia_tipo: terapiaTipo,
        criterios_pesos: criteriosPesos
      }
    );
  }

  /**
   * Flujo completo: Actividades + Terapeuta + Explicaciones
   */
  getRecomendacionCompleta(
    ninoId: number,
    terapiaTipo: string
  ): Observable<any> {
    return this.http.post<any>(
      `${this.API_RECOMENDACIONES}/completa/${ninoId}`,
      { terapia_tipo: terapiaTipo }
    );
  }

  /**
   * Registra el progreso de una actividad
   */
  registrarProgreso(data: {
    nino_id: number;
    actividad_id: number;
    terapeuta_id: number;
    calificacion: number;
    notas_progreso?: string;
    duracion_minutos?: number;
  }): Observable<any> {
    return this.http.post<any>(
      `${this.API_RECOMENDACIONES}/progreso/registrar`,
      data
    );
  }

  /**
   * Genera sugerencias clínicas con Gemini
   */
  getSugerenciasClinicas(
    ninoId: number,
    incluirActividadesActuales: boolean = true,
    incluirProgresoReciente: boolean = true
  ): Observable<any> {
    return this.http.post<any>(
      `${this.API_RECOMENDACIONES}/sugerencias/${ninoId}`,
      {
        incluir_actividades_actuales: incluirActividadesActuales,
        incluir_progreso_reciente: incluirProgresoReciente
      }
    );
  }

  /**
   * Obtiene el historial de recomendaciones
   */
  getHistorialRecomendaciones(
    ninoId: number,
    limite: number = 10
  ): Observable<any> {
    const params = new HttpParams().set('limite', limite.toString());
    return this.http.get<any>(
      `${this.API_RECOMENDACIONES}/historial/${ninoId}`,
      { params }
    );
  }

  // ============================================================
  // MÉTODOS PARA PADRES (COMPATIBILIDAD CON CÓDIGO EXISTENTE)
  // ============================================================

  /**
   * Obtiene recomendaciones para padres
   */
  obtenerRecomendaciones(idNino: number): Observable<RecursoRecomendado[]> {
    return this.http.get<RecursoRecomendado[]>(
      `${this.API_PADRES}/${idNino}/recomendaciones`
    );
  }
}




