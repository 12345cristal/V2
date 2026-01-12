import { Injectable } from '@angular/core';
import { HttpClient, HttpErrorResponse, HttpParams } from '@angular/common/http';
import { Observable, throwError } from 'rxjs';
import { catchError, map } from 'rxjs/operators';
import { environment } from '../../enviroment/environment';
import {
  ISesion,
  ITipoTerapia,
  IEstadoSesion,
  IBitacoraDaily,
  IGrabacionVoz
} from '../interfaces/sesiones.interface';
import { IResponse, IResponsePaginado } from '../interfaces/shared.interface';

/**
 * Servicio para la gestión de sesiones terapéuticas
 * Proporciona métodos CRUD para sesiones y bitácoras
 */
@Injectable({
  providedIn: 'root'
})
export class SesionesService {
  private readonly baseUrl = `${environment.apiBaseUrl}/sesiones`;

  constructor(private http: HttpClient) {}

  /**
   * Obtiene la lista de sesiones del padre
   * @param padreId ID del padre
   * @param filtros Filtros opcionales (estado, fechaDesde, fechaHasta, etc.)
   * @param page Número de página
   * @param pageSize Tamaño de página
   * @returns Observable con las sesiones paginadas
   */
  getSesiones(
    padreId: number,
    filtros?: {
      estado?: IEstadoSesion;
      tipoTerapia?: ITipoTerapia;
      ninoId?: number;
      fechaDesde?: string;
      fechaHasta?: string;
    },
    page: number = 1,
    pageSize: number = 20
  ): Observable<IResponsePaginado<ISesion>> {
    let params = new HttpParams()
      .set('padreId', padreId.toString())
      .set('page', page.toString())
      .set('pageSize', pageSize.toString());

    if (filtros) {
      if (filtros.estado) params = params.set('estado', filtros.estado);
      if (filtros.tipoTerapia) params = params.set('tipoTerapia', filtros.tipoTerapia);
      if (filtros.ninoId) params = params.set('ninoId', filtros.ninoId.toString());
      if (filtros.fechaDesde) params = params.set('fechaDesde', filtros.fechaDesde);
      if (filtros.fechaHasta) params = params.set('fechaHasta', filtros.fechaHasta);
    }

    return this.http.get<IResponsePaginado<ISesion>>(this.baseUrl, { params })
      .pipe(catchError(this.handleError));
  }

  /**
   * Obtiene una sesión por su ID
   * @param sesionId ID de la sesión
   * @returns Observable con la sesión
   */
  getSesion(sesionId: number): Observable<ISesion> {
    return this.http.get<IResponse<ISesion>>(`${this.baseUrl}/${sesionId}`)
      .pipe(
        map(response => response.data!),
        catchError(this.handleError)
      );
  }

  /**
   * Confirma la asistencia a una sesión
   * @param sesionId ID de la sesión
   * @returns Observable con la sesión actualizada
   */
  confirmarAsistencia(sesionId: number): Observable<ISesion> {
    return this.http.patch<IResponse<ISesion>>(
      `${this.baseUrl}/${sesionId}/confirmar`,
      {}
    ).pipe(
      map(response => response.data!),
      catchError(this.handleError)
    );
  }

  /**
   * Cancela una sesión
   * @param sesionId ID de la sesión
   * @param motivo Motivo de la cancelación
   * @returns Observable con la sesión actualizada
   */
  cancelarSesion(sesionId: number, motivo: string): Observable<ISesion> {
    return this.http.patch<IResponse<ISesion>>(
      `${this.baseUrl}/${sesionId}/cancelar`,
      { motivo }
    ).pipe(
      map(response => response.data!),
      catchError(this.handleError)
    );
  }

  /**
   * Solicita reprogramación de una sesión
   * @param sesionId ID de la sesión
   * @param nuevaFecha Nueva fecha propuesta
   * @param motivo Motivo de la reprogramación
   * @returns Observable con la confirmación
   */
  solicitarReprogramacion(
    sesionId: number,
    nuevaFecha: string,
    motivo: string
  ): Observable<void> {
    return this.http.post<IResponse<void>>(
      `${this.baseUrl}/${sesionId}/reprogramar`,
      { nuevaFecha, motivo }
    ).pipe(
      map(() => undefined),
      catchError(this.handleError)
    );
  }

  /**
   * Obtiene la bitácora de una sesión
   * @param sesionId ID de la sesión
   * @returns Observable con la bitácora
   */
  getBitacora(sesionId: number): Observable<IBitacoraDaily | null> {
    return this.http.get<IResponse<IBitacoraDaily>>(`${this.baseUrl}/${sesionId}/bitacora`)
      .pipe(
        map(response => response.data || null),
        catchError(this.handleError)
      );
  }

  /**
   * Obtiene las grabaciones de una sesión
   * @param sesionId ID de la sesión
   * @returns Observable con la lista de grabaciones
   */
  getGrabaciones(sesionId: number): Observable<IGrabacionVoz[]> {
    return this.http.get<IResponse<IGrabacionVoz[]>>(`${this.baseUrl}/${sesionId}/grabaciones`)
      .pipe(
        map(response => response.data || []),
        catchError(this.handleError)
      );
  }

  /**
   * Obtiene las próximas sesiones del padre
   * @param padreId ID del padre
   * @param limit Número máximo de sesiones a devolver
   * @returns Observable con las próximas sesiones
   */
  getProximasSesiones(padreId: number, limit: number = 5): Observable<ISesion[]> {
    const params = new HttpParams()
      .set('padreId', padreId.toString())
      .set('limit', limit.toString())
      .set('estado', IEstadoSesion.PROGRAMADA);

    return this.http.get<IResponse<ISesion[]>>(`${this.baseUrl}/proximas`, { params })
      .pipe(
        map(response => response.data || []),
        catchError(this.handleError)
      );
  }

  /**
   * Obtiene el historial de sesiones completadas
   * @param ninoId ID del niño
   * @param page Número de página
   * @param pageSize Tamaño de página
   * @returns Observable con las sesiones completadas paginadas
   */
  getHistorialSesiones(
    ninoId: number,
    page: number = 1,
    pageSize: number = 20
  ): Observable<IResponsePaginado<ISesion>> {
    const params = new HttpParams()
      .set('ninoId', ninoId.toString())
      .set('estado', IEstadoSesion.COMPLETADA)
      .set('page', page.toString())
      .set('pageSize', pageSize.toString());

    return this.http.get<IResponsePaginado<ISesion>>(this.baseUrl, { params })
      .pipe(catchError(this.handleError));
  }

  /**
   * Maneja los errores HTTP
   * @param error Error HTTP
   * @returns Observable con el error
   */
  private handleError(error: HttpErrorResponse): Observable<never> {
    let errorMessage = 'Ocurrió un error desconocido';
    
    if (error.error instanceof ErrorEvent) {
      errorMessage = `Error: ${error.error.message}`;
    } else {
      errorMessage = error.error?.message || `Error del servidor: ${error.status}`;
    }
    
    console.error('Error en SesionesService:', errorMessage);
    return throwError(() => new Error(errorMessage));
  }
}
