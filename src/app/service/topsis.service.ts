import { Injectable, inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../enviroment/environment';
import { 
  CriterioTopsis, 
  TopsisInput, 
  TopsisResultado,
  TopsisRequest 
} from '../interfaces/topsis.interface';

/**
 * Servicio para gestión de TOPSIS
 * Permite al coordinador gestionar criterios y calcular prioridad de niños/terapeutas
 */
@Injectable({ providedIn: 'root' })
export class TopsisService {
  private http = inject(HttpClient);
  private readonly API_URL = `${environment.apiBaseUrl}/topsis`;
  private readonly API_COORD = `${environment.apiBaseUrl}/coordinador/topsis`;

  // ============================================================
  // MÉTODOS PARA GESTIÓN DE CRITERIOS TOPSIS
  // ============================================================

  /**
   * Obtiene todos los criterios TOPSIS
   */
  getCriteriosTopsis(incluirInactivos: boolean = false): Observable<CriterioTopsis[]> {
    const url = `${this.API_URL}/criterios?incluir_inactivos=${incluirInactivos}`;
    return this.http.get<CriterioTopsis[]>(url);
  }

  /**
   * Crea un nuevo criterio TOPSIS
   */
  createCriterioTopsis(criterio: CriterioTopsis): Observable<CriterioTopsis> {
    return this.http.post<CriterioTopsis>(`${this.API_URL}/criterios`, criterio);
  }

  /**
   * Actualiza un criterio TOPSIS existente
   */
  updateCriterioTopsis(id: number, criterio: Partial<CriterioTopsis>): Observable<CriterioTopsis> {
    return this.http.put<CriterioTopsis>(`${this.API_URL}/criterios/${id}`, criterio);
  }

  /**
   * Elimina un criterio TOPSIS
   */
  deleteCriterioTopsis(id: number): Observable<void> {
    return this.http.delete<void>(`${this.API_URL}/criterios/${id}`);
  }

  /**
   * Calcula la prioridad de niños usando TOPSIS
   * @param payload Objeto con ids de niños y matriz de decisión
   */
  calcularPrioridadNinos(payload: TopsisInput): Observable<TopsisResultado[]> {
    return this.http.post<TopsisResultado[]>(`${this.API_URL}/prioridad-ninos`, payload);
  }

  // ============================================================
  // MÉTODOS PROFESIONALES PARA EVALUACIÓN DE TERAPEUTAS
  // ============================================================

  /**
   * Evalúa terapeutas usando TOPSIS con pesos configurables
   * @param request Configuración de evaluación con pesos y filtros
   * @returns Observable con ranking de terapeutas calculado
   */
  evaluarTerapeutasProfesional(request: any): Observable<any> {
    return this.http.post<any>(`${this.API_URL}/terapeutas`, request);
  }

  /**
   * Obtiene la configuración de pesos por defecto
   * @returns Observable con pesos default y descripciones
   */
  obtenerPesosDefault(): Observable<any> {
    return this.http.get<any>(`${this.API_URL}/terapeutas/pesos-default`);
  }

  // ============================================================
  // MÉTODOS LEGACY (mantener por compatibilidad)
  // ============================================================

  /**
   * Evalúa terapeutas usando TOPSIS
   * @deprecated Usar evaluarTerapeutasProfesional en su lugar
   */
  evaluarTerapeutas(payload: TopsisInput): Observable<TopsisResultado[]> {
    return this.http.post<TopsisResultado[]>(`${this.API_URL}/evaluar-terapeutas`, payload);
  }

  /**
   * Obtiene la matriz de terapeutas automáticamente desde el backend
   * @deprecated Usar evaluarTerapeutasProfesional con pesos default
   */
  obtenerMatrizTerapeutas(): Observable<any> {
    return this.http.get<any>(`${this.API_URL}/matriz-terapeutas`);
  }
}
