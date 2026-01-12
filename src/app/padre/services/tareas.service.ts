import { Injectable } from '@angular/core';
import { HttpClient, HttpErrorResponse, HttpParams } from '@angular/common/http';
import { Observable, throwError } from 'rxjs';
import { catchError, map } from 'rxjs/operators';
import { environment } from '../../enviroment/environment';
import { ITarea, IEstadoTarea, IRecursoAsociado } from '../interfaces/tareas.interface';
import { IResponse, IResponsePaginado } from '../interfaces/shared.interface';

/**
 * Servicio para la gestión de tareas asignadas
 * Proporciona métodos CRUD para tareas
 */
@Injectable({
  providedIn: 'root'
})
export class TareasService {
  private readonly baseUrl = `${environment.apiBaseUrl}/tareas`;

  constructor(private http: HttpClient) {}

  /**
   * Obtiene la lista de tareas del padre
   * @param padreId ID del padre
   * @param filtros Filtros opcionales
   * @param page Número de página
   * @param pageSize Tamaño de página
   * @returns Observable con las tareas paginadas
   */
  getTareas(
    padreId: number,
    filtros?: {
      estado?: IEstadoTarea;
      ninoId?: number;
      prioridad?: string;
      fechaDesde?: string;
      fechaHasta?: string;
    },
    page: number = 1,
    pageSize: number = 20
  ): Observable<IResponsePaginado<ITarea>> {
    let params = new HttpParams()
      .set('padreId', padreId.toString())
      .set('page', page.toString())
      .set('pageSize', pageSize.toString());

    if (filtros) {
      if (filtros.estado) params = params.set('estado', filtros.estado);
      if (filtros.ninoId) params = params.set('ninoId', filtros.ninoId.toString());
      if (filtros.prioridad) params = params.set('prioridad', filtros.prioridad);
      if (filtros.fechaDesde) params = params.set('fechaDesde', filtros.fechaDesde);
      if (filtros.fechaHasta) params = params.set('fechaHasta', filtros.fechaHasta);
    }

    return this.http.get<IResponsePaginado<ITarea>>(this.baseUrl, { params })
      .pipe(catchError(this.handleError));
  }

  /**
   * Obtiene una tarea por su ID
   * @param tareaId ID de la tarea
   * @returns Observable con la tarea
   */
  getTarea(tareaId: number): Observable<ITarea> {
    return this.http.get<IResponse<ITarea>>(`${this.baseUrl}/${tareaId}`)
      .pipe(
        map(response => response.data!),
        catchError(this.handleError)
      );
  }

  /**
   * Marca una tarea como completada
   * @param tareaId ID de la tarea
   * @param comentarios Comentarios adicionales (opcional)
   * @returns Observable con la tarea actualizada
   */
  completarTarea(tareaId: number, comentarios?: string): Observable<ITarea> {
    return this.http.patch<IResponse<ITarea>>(
      `${this.baseUrl}/${tareaId}/completar`,
      { comentarios }
    ).pipe(
      map(response => response.data!),
      catchError(this.handleError)
    );
  }

  /**
   * Reporta progreso en una tarea
   * @param tareaId ID de la tarea
   * @param progreso Datos del progreso
   * @returns Observable con la tarea actualizada
   */
  reportarProgreso(
    tareaId: number,
    progreso: {
      descripcion: string;
      dificultades?: string;
      evidencia?: File[];
    }
  ): Observable<ITarea> {
    const formData = new FormData();
    formData.append('descripcion', progreso.descripcion);
    if (progreso.dificultades) formData.append('dificultades', progreso.dificultades);
    
    if (progreso.evidencia && progreso.evidencia.length > 0) {
      progreso.evidencia.forEach((archivo, index) => {
        formData.append(`evidencia[${index}]`, archivo);
      });
    }

    return this.http.post<IResponse<ITarea>>(
      `${this.baseUrl}/${tareaId}/progreso`,
      formData
    ).pipe(
      map(response => response.data!),
      catchError(this.handleError)
    );
  }

  /**
   * Obtiene tareas pendientes del padre
   * @param padreId ID del padre
   * @param limit Número máximo de tareas
   * @returns Observable con las tareas pendientes
   */
  getTareasPendientes(padreId: number, limit: number = 10): Observable<ITarea[]> {
    const params = new HttpParams()
      .set('padreId', padreId.toString())
      .set('estado', IEstadoTarea.PENDIENTE)
      .set('limit', limit.toString());

    return this.http.get<IResponse<ITarea[]>>(`${this.baseUrl}/pendientes`, { params })
      .pipe(
        map(response => response.data || []),
        catchError(this.handleError)
      );
  }

  /**
   * Obtiene tareas vencidas del padre
   * @param padreId ID del padre
   * @returns Observable con las tareas vencidas
   */
  getTareasVencidas(padreId: number): Observable<ITarea[]> {
    const params = new HttpParams()
      .set('padreId', padreId.toString())
      .set('estado', IEstadoTarea.VENCIDA);

    return this.http.get<IResponse<ITarea[]>>(`${this.baseUrl}/vencidas`, { params })
      .pipe(
        map(response => response.data || []),
        catchError(this.handleError)
      );
  }

  /**
   * Cambia el estado de notificaciones de una tarea
   * @param tareaId ID de la tarea
   * @param activar Si es true activa notificaciones, si es false las desactiva
   * @returns Observable con la tarea actualizada
   */
  configurarNotificaciones(tareaId: number, activar: boolean): Observable<ITarea> {
    return this.http.patch<IResponse<ITarea>>(
      `${this.baseUrl}/${tareaId}/notificaciones`,
      { notificacionesActivas: activar }
    ).pipe(
      map(response => response.data!),
      catchError(this.handleError)
    );
  }

  /**
   * Obtiene el historial de tareas completadas
   * @param ninoId ID del niño
   * @param page Número de página
   * @param pageSize Tamaño de página
   * @returns Observable con las tareas completadas paginadas
   */
  getHistorialTareas(
    ninoId: number,
    page: number = 1,
    pageSize: number = 20
  ): Observable<IResponsePaginado<ITarea>> {
    const params = new HttpParams()
      .set('ninoId', ninoId.toString())
      .set('estado', IEstadoTarea.COMPLETADA)
      .set('page', page.toString())
      .set('pageSize', pageSize.toString());

    return this.http.get<IResponsePaginado<ITarea>>(this.baseUrl, { params })
      .pipe(catchError(this.handleError));
  }

  /**
   * Descarga un recurso asociado a la tarea
   * @param recursoId ID del recurso
   * @returns Observable con el blob del archivo
   */
  descargarRecurso(recursoId: number): Observable<Blob> {
    return this.http.get(`${this.baseUrl}/recursos/${recursoId}/descargar`, {
      responseType: 'blob'
    }).pipe(catchError(this.handleError));
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
    
    console.error('Error en TareasService:', errorMessage);
    return throwError(() => new Error(errorMessage));
  }
}
