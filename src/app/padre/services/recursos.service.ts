import { Injectable } from '@angular/core';
import { HttpClient, HttpErrorResponse, HttpParams } from '@angular/common/http';
import { Observable, throwError } from 'rxjs';
import { catchError, map } from 'rxjs/operators';
import { environment } from '../../enviroment/environment';
import { IRecurso, ITipoRecurso } from '../interfaces/recursos.interface';
import { IResponse, IResponsePaginado } from '../interfaces/shared.interface';

/**
 * Servicio para la gestión de recursos educativos
 * Proporciona métodos para acceder y gestionar recursos
 */
@Injectable({
  providedIn: 'root'
})
export class RecursosService {
  private readonly baseUrl = `${environment.apiBaseUrl}/recursos`;

  constructor(private http: HttpClient) {}

  /**
   * Obtiene la lista de recursos disponibles
   * @param filtros Filtros opcionales
   * @param page Número de página
   * @param pageSize Tamaño de página
   * @returns Observable con los recursos paginados
   */
  getRecursos(
    filtros?: {
      tipo?: ITipoRecurso;
      categoria?: string;
      etiquetas?: string[];
      nivelDificultad?: string;
      idioma?: string;
      favoritos?: boolean;
    },
    page: number = 1,
    pageSize: number = 20
  ): Observable<IResponsePaginado<IRecurso>> {
    let params = new HttpParams()
      .set('page', page.toString())
      .set('pageSize', pageSize.toString());

    if (filtros) {
      if (filtros.tipo) params = params.set('tipo', filtros.tipo);
      if (filtros.categoria) params = params.set('categoria', filtros.categoria);
      if (filtros.etiquetas) params = params.set('etiquetas', filtros.etiquetas.join(','));
      if (filtros.nivelDificultad) params = params.set('nivelDificultad', filtros.nivelDificultad);
      if (filtros.idioma) params = params.set('idioma', filtros.idioma);
      if (filtros.favoritos !== undefined) params = params.set('favoritos', filtros.favoritos.toString());
    }

    return this.http.get<IResponsePaginado<IRecurso>>(this.baseUrl, { params })
      .pipe(catchError(this.handleError));
  }

  /**
   * Obtiene un recurso por su ID
   * @param recursoId ID del recurso
   * @returns Observable con el recurso
   */
  getRecurso(recursoId: number): Observable<IRecurso> {
    return this.http.get<IResponse<IRecurso>>(`${this.baseUrl}/${recursoId}`)
      .pipe(
        map(response => response.data!),
        catchError(this.handleError)
      );
  }

  /**
   * Obtiene recursos recomendados para un niño
   * @param ninoId ID del niño
   * @param limit Número máximo de recursos
   * @returns Observable con los recursos recomendados
   */
  getRecursosRecomendados(ninoId: number, limit: number = 10): Observable<IRecurso[]> {
    const params = new HttpParams()
      .set('ninoId', ninoId.toString())
      .set('limit', limit.toString());

    return this.http.get<IResponse<IRecurso[]>>(`${this.baseUrl}/recomendados`, { params })
      .pipe(
        map(response => response.data || []),
        catchError(this.handleError)
      );
  }

  /**
   * Marca un recurso como favorito
   * @param recursoId ID del recurso
   * @param usuarioId ID del usuario
   * @returns Observable con el recurso actualizado
   */
  marcarFavorito(recursoId: number, usuarioId: number): Observable<IRecurso> {
    return this.http.post<IResponse<IRecurso>>(
      `${this.baseUrl}/${recursoId}/favorito`,
      { usuarioId }
    ).pipe(
      map(response => response.data!),
      catchError(this.handleError)
    );
  }

  /**
   * Quita un recurso de favoritos
   * @param recursoId ID del recurso
   * @param usuarioId ID del usuario
   * @returns Observable con el recurso actualizado
   */
  quitarFavorito(recursoId: number, usuarioId: number): Observable<IRecurso> {
    return this.http.delete<IResponse<IRecurso>>(
      `${this.baseUrl}/${recursoId}/favorito`,
      { params: new HttpParams().set('usuarioId', usuarioId.toString()) }
    ).pipe(
      map(response => response.data!),
      catchError(this.handleError)
    );
  }

  /**
   * Marca un recurso como completado
   * @param recursoId ID del recurso
   * @param usuarioId ID del usuario
   * @param progreso Progreso alcanzado (0-100)
   * @returns Observable con el recurso actualizado
   */
  marcarCompletado(
    recursoId: number,
    usuarioId: number,
    progreso: number = 100
  ): Observable<IRecurso> {
    return this.http.post<IResponse<IRecurso>>(
      `${this.baseUrl}/${recursoId}/completado`,
      { usuarioId, progreso }
    ).pipe(
      map(response => response.data!),
      catchError(this.handleError)
    );
  }

  /**
   * Actualiza el progreso en un recurso
   * @param recursoId ID del recurso
   * @param usuarioId ID del usuario
   * @param progreso Progreso alcanzado (0-100)
   * @returns Observable con el recurso actualizado
   */
  actualizarProgreso(
    recursoId: number,
    usuarioId: number,
    progreso: number
  ): Observable<IRecurso> {
    return this.http.patch<IResponse<IRecurso>>(
      `${this.baseUrl}/${recursoId}/progreso`,
      { usuarioId, progreso }
    ).pipe(
      map(response => response.data!),
      catchError(this.handleError)
    );
  }

  /**
   * Califica un recurso
   * @param recursoId ID del recurso
   * @param usuarioId ID del usuario
   * @param calificacion Calificación (1-5)
   * @returns Observable con el recurso actualizado
   */
  calificarRecurso(
    recursoId: number,
    usuarioId: number,
    calificacion: number
  ): Observable<IRecurso> {
    return this.http.post<IResponse<IRecurso>>(
      `${this.baseUrl}/${recursoId}/calificar`,
      { usuarioId, calificacion }
    ).pipe(
      map(response => response.data!),
      catchError(this.handleError)
    );
  }

  /**
   * Registra una visualización o descarga del recurso
   * @param recursoId ID del recurso
   * @param tipo Tipo de acción ('visualizacion' | 'descarga')
   * @returns Observable con la confirmación
   */
  registrarAccion(recursoId: number, tipo: 'visualizacion' | 'descarga'): Observable<void> {
    return this.http.post<IResponse<void>>(
      `${this.baseUrl}/${recursoId}/accion`,
      { tipo }
    ).pipe(
      map(() => undefined),
      catchError(this.handleError)
    );
  }

  /**
   * Agrega notas a un recurso
   * @param recursoId ID del recurso
   * @param usuarioId ID del usuario
   * @param notas Notas del usuario
   * @returns Observable con el recurso actualizado
   */
  agregarNotas(recursoId: number, usuarioId: number, notas: string): Observable<IRecurso> {
    return this.http.patch<IResponse<IRecurso>>(
      `${this.baseUrl}/${recursoId}/notas`,
      { usuarioId, notas }
    ).pipe(
      map(response => response.data!),
      catchError(this.handleError)
    );
  }

  /**
   * Busca recursos por término
   * @param termino Término de búsqueda
   * @returns Observable con los recursos encontrados
   */
  buscarRecursos(termino: string): Observable<IRecurso[]> {
    const params = new HttpParams().set('q', termino);
    return this.http.get<IResponse<IRecurso[]>>(`${this.baseUrl}/buscar`, { params })
      .pipe(
        map(response => response.data || []),
        catchError(this.handleError)
      );
  }

  /**
   * Obtiene las categorías disponibles
   * @returns Observable con la lista de categorías
   */
  getCategorias(): Observable<string[]> {
    return this.http.get<IResponse<string[]>>(`${this.baseUrl}/categorias`)
      .pipe(
        map(response => response.data || []),
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
      errorMessage = `Error: ${error.error.message}`;
    } else {
      errorMessage = error.error?.message || `Error del servidor: ${error.status}`;
    }
    
    console.error('Error en RecursosService:', errorMessage);
    return throwError(() => new Error(errorMessage));
  }
}
