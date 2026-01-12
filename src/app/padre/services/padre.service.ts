import { Injectable } from '@angular/core';
import { HttpClient, HttpErrorResponse, HttpParams } from '@angular/common/http';
import { Observable, throwError } from 'rxjs';
import { catchError, map } from 'rxjs/operators';
import { environment } from '../../enviroment/environment';
import {
  IDashboardResumen,
  IProximaSesion,
  IUltimoAvance,
  IPagosPendientes,
  IDocumentoNuevo,
  IObservacionTerapeuta
} from '../interfaces/dashboard.interface';
import { IHijo } from '../interfaces/mis-hijos.interface';
import { IResponse, IResponsePaginado } from '../interfaces/shared.interface';

/**
 * Servicio principal para la gestión del módulo Padre
 * Proporciona métodos para obtener información del dashboard y gestionar hijos
 */
@Injectable({
  providedIn: 'root'
})
export class PadreService {
  private readonly baseUrl = `${environment.apiBaseUrl}/padre`;

  constructor(private http: HttpClient) {}

  /**
   * Obtiene el resumen del dashboard para el padre
   * @param padreId ID del padre
   * @returns Observable con el resumen del dashboard
   */
  getDashboardResumen(padreId: number): Observable<IDashboardResumen> {
    return this.http.get<IResponse<IDashboardResumen>>(`${this.baseUrl}/${padreId}/dashboard`)
      .pipe(
        map(response => response.data!),
        catchError(this.handleError)
      );
  }

  /**
   * Obtiene la próxima sesión programada
   * @param padreId ID del padre
   * @returns Observable con la información de la próxima sesión
   */
  getProximaSesion(padreId: number): Observable<IProximaSesion | null> {
    return this.http.get<IResponse<IProximaSesion>>(`${this.baseUrl}/${padreId}/proxima-sesion`)
      .pipe(
        map(response => response.data || null),
        catchError(this.handleError)
      );
  }

  /**
   * Obtiene el último avance registrado
   * @param padreId ID del padre
   * @returns Observable con el último avance
   */
  getUltimoAvance(padreId: number): Observable<IUltimoAvance | null> {
    return this.http.get<IResponse<IUltimoAvance>>(`${this.baseUrl}/${padreId}/ultimo-avance`)
      .pipe(
        map(response => response.data || null),
        catchError(this.handleError)
      );
  }

  /**
   * Obtiene los pagos pendientes del padre
   * @param padreId ID del padre
   * @returns Observable con la lista de pagos pendientes
   */
  getPagosPendientes(padreId: number): Observable<IPagosPendientes[]> {
    return this.http.get<IResponse<IPagosPendientes[]>>(`${this.baseUrl}/${padreId}/pagos-pendientes`)
      .pipe(
        map(response => response.data || []),
        catchError(this.handleError)
      );
  }

  /**
   * Obtiene los documentos nuevos sin revisar
   * @param padreId ID del padre
   * @returns Observable con la lista de documentos nuevos
   */
  getDocumentosNuevos(padreId: number): Observable<IDocumentoNuevo[]> {
    return this.http.get<IResponse<IDocumentoNuevo[]>>(`${this.baseUrl}/${padreId}/documentos-nuevos`)
      .pipe(
        map(response => response.data || []),
        catchError(this.handleError)
      );
  }

  /**
   * Obtiene las observaciones del terapeuta
   * @param padreId ID del padre
   * @param pendientesOnly Si es true, solo devuelve observaciones no leídas
   * @returns Observable con la lista de observaciones
   */
  getObservacionesTerapeuta(padreId: number, pendientesOnly: boolean = false): Observable<IObservacionTerapeuta[]> {
    const params = new HttpParams().set('pendientesOnly', pendientesOnly.toString());
    return this.http.get<IResponse<IObservacionTerapeuta[]>>(
      `${this.baseUrl}/${padreId}/observaciones-terapeuta`,
      { params }
    ).pipe(
      map(response => response.data || []),
      catchError(this.handleError)
    );
  }

  /**
   * Marca una observación como leída
   * @param observacionId ID de la observación
   * @returns Observable con la confirmación
   */
  marcarObservacionLeida(observacionId: number): Observable<void> {
    return this.http.patch<IResponse<void>>(
      `${this.baseUrl}/observaciones/${observacionId}/marcar-leida`,
      {}
    ).pipe(
      map(() => undefined),
      catchError(this.handleError)
    );
  }

  /**
   * Obtiene la lista de hijos del padre
   * @param padreId ID del padre
   * @param activos Si es true, solo devuelve hijos activos
   * @returns Observable con la lista de hijos
   */
  getHijos(padreId: number, activos: boolean = true): Observable<IHijo[]> {
    const params = new HttpParams().set('activos', activos.toString());
    return this.http.get<IResponse<IHijo[]>>(`${this.baseUrl}/${padreId}/hijos`, { params })
      .pipe(
        map(response => response.data || []),
        catchError(this.handleError)
      );
  }

  /**
   * Obtiene la información detallada de un hijo
   * @param hijoId ID del hijo
   * @returns Observable con la información del hijo
   */
  getHijo(hijoId: number): Observable<IHijo> {
    return this.http.get<IResponse<IHijo>>(`${this.baseUrl}/hijos/${hijoId}`)
      .pipe(
        map(response => response.data!),
        catchError(this.handleError)
      );
  }

  /**
   * Actualiza la información de un hijo
   * @param hijoId ID del hijo
   * @param data Datos a actualizar
   * @returns Observable con la información actualizada del hijo
   */
  actualizarHijo(hijoId: number, data: Partial<IHijo>): Observable<IHijo> {
    return this.http.put<IResponse<IHijo>>(`${this.baseUrl}/hijos/${hijoId}`, data)
      .pipe(
        map(response => response.data!),
        catchError(this.handleError)
      );
  }

  /**
   * Maneja los errores HTTP
   * @param error Error HTTP
   * @returns Observable con el error
   */
  private handleError(error: HttpErrorResponse): Observable<never> {
    let errorMessage = 'Ocurrió un error desconocido';
    
    if (error.error instanceof ErrorEvent) {
      // Error del lado del cliente
      errorMessage = `Error: ${error.error.message}`;
    } else {
      // Error del lado del servidor
      errorMessage = error.error?.message || `Error del servidor: ${error.status}`;
    }
    
    console.error('Error en PadreService:', errorMessage);
    return throwError(() => new Error(errorMessage));
  }
}
