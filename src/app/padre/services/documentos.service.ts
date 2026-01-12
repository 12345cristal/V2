import { Injectable } from '@angular/core';
import { HttpClient, HttpErrorResponse, HttpParams } from '@angular/common/http';
import { Observable, throwError } from 'rxjs';
import { catchError, map } from 'rxjs/operators';
import { environment } from '../../enviroment/environment';
import { IDocumento, ITipoDocumento } from '../interfaces/documentos.interface';
import { IResponse, IResponsePaginado } from '../interfaces/shared.interface';

/**
 * Servicio para la gestión de documentos del módulo padre
 * Proporciona métodos CRUD para documentos
 */
@Injectable({
  providedIn: 'root'
})
export class DocumentosPadreService {
  private readonly baseUrl = `${environment.apiBaseUrl}/documentos`;

  constructor(private http: HttpClient) {}

  /**
   * Obtiene la lista de documentos
   * @param padreId ID del padre
   * @param filtros Filtros opcionales
   * @param page Número de página
   * @param pageSize Tamaño de página
   * @returns Observable con los documentos paginados
   */
  getDocumentos(
    padreId: number,
    filtros?: {
      ninoId?: number;
      tipo?: ITipoDocumento;
      subidoPor?: string;
      fechaDesde?: string;
      fechaHasta?: string;
    },
    page: number = 1,
    pageSize: number = 20
  ): Observable<IResponsePaginado<IDocumento>> {
    let params = new HttpParams()
      .set('padreId', padreId.toString())
      .set('page', page.toString())
      .set('pageSize', pageSize.toString());

    if (filtros) {
      if (filtros.ninoId) params = params.set('ninoId', filtros.ninoId.toString());
      if (filtros.tipo) params = params.set('tipo', filtros.tipo);
      if (filtros.subidoPor) params = params.set('subidoPor', filtros.subidoPor);
      if (filtros.fechaDesde) params = params.set('fechaDesde', filtros.fechaDesde);
      if (filtros.fechaHasta) params = params.set('fechaHasta', filtros.fechaHasta);
    }

    return this.http.get<IResponsePaginado<IDocumento>>(this.baseUrl, { params })
      .pipe(catchError(this.handleError));
  }

  /**
   * Obtiene un documento por su ID
   * @param documentoId ID del documento
   * @returns Observable con el documento
   */
  getDocumento(documentoId: number): Observable<IDocumento> {
    return this.http.get<IResponse<IDocumento>>(`${this.baseUrl}/${documentoId}`)
      .pipe(
        map(response => response.data!),
        catchError(this.handleError)
      );
  }

  /**
   * Sube un nuevo documento
   * @param data Datos del documento
   * @param archivo Archivo a subir
   * @returns Observable con el documento creado
   */
  subirDocumento(
    data: {
      ninoId: number;
      titulo: string;
      descripcion?: string;
      tipo: ITipoDocumento;
      parentesco?: string;
      visiblePara?: {
        padres: boolean;
        terapeutas: boolean;
        coordinadores: boolean;
        administradores: boolean;
      };
      etiquetas?: string[];
      privado?: boolean;
    },
    archivo: File
  ): Observable<IDocumento> {
    const formData = new FormData();
    formData.append('archivo', archivo);
    formData.append('ninoId', data.ninoId.toString());
    formData.append('titulo', data.titulo);
    if (data.descripcion) formData.append('descripcion', data.descripcion);
    formData.append('tipo', data.tipo);
    if (data.parentesco) formData.append('parentesco', data.parentesco);
    if (data.visiblePara) formData.append('visiblePara', JSON.stringify(data.visiblePara));
    if (data.etiquetas) formData.append('etiquetas', JSON.stringify(data.etiquetas));
    if (data.privado !== undefined) formData.append('privado', data.privado.toString());

    return this.http.post<IResponse<IDocumento>>(this.baseUrl, formData)
      .pipe(
        map(response => response.data!),
        catchError(this.handleError)
      );
  }

  /**
   * Actualiza un documento
   * @param documentoId ID del documento
   * @param data Datos a actualizar
   * @returns Observable con el documento actualizado
   */
  actualizarDocumento(
    documentoId: number,
    data: Partial<IDocumento>
  ): Observable<IDocumento> {
    return this.http.put<IResponse<IDocumento>>(`${this.baseUrl}/${documentoId}`, data)
      .pipe(
        map(response => response.data!),
        catchError(this.handleError)
      );
  }

  /**
   * Elimina un documento
   * @param documentoId ID del documento
   * @returns Observable con la confirmación
   */
  eliminarDocumento(documentoId: number): Observable<void> {
    return this.http.delete<IResponse<void>>(`${this.baseUrl}/${documentoId}`)
      .pipe(
        map(() => undefined),
        catchError(this.handleError)
      );
  }

  /**
   * Descarga un documento
   * @param documentoId ID del documento
   * @returns Observable con el blob del archivo
   */
  descargarDocumento(documentoId: number): Observable<Blob> {
    return this.http.get(`${this.baseUrl}/${documentoId}/descargar`, {
      responseType: 'blob'
    }).pipe(catchError(this.handleError));
  }

  /**
   * Marca un documento como visto
   * @param documentoId ID del documento
   * @returns Observable con el documento actualizado
   */
  marcarComoVisto(documentoId: number): Observable<IDocumento> {
    return this.http.patch<IResponse<IDocumento>>(
      `${this.baseUrl}/${documentoId}/visto`,
      {}
    ).pipe(
      map(response => response.data!),
      catchError(this.handleError)
    );
  }

  /**
   * Archiva un documento
   * @param documentoId ID del documento
   * @returns Observable con el documento actualizado
   */
  archivarDocumento(documentoId: number): Observable<IDocumento> {
    return this.http.patch<IResponse<IDocumento>>(
      `${this.baseUrl}/${documentoId}/archivar`,
      {}
    ).pipe(
      map(response => response.data!),
      catchError(this.handleError)
    );
  }

  /**
   * Busca documentos por título o etiquetas
   * @param termino Término de búsqueda
   * @param padreId ID del padre
   * @returns Observable con los documentos encontrados
   */
  buscarDocumentos(termino: string, padreId: number): Observable<IDocumento[]> {
    const params = new HttpParams()
      .set('q', termino)
      .set('padreId', padreId.toString());

    return this.http.get<IResponse<IDocumento[]>>(`${this.baseUrl}/buscar`, { params })
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
    
    console.error('Error en DocumentosPadreService:', errorMessage);
    return throwError(() => new Error(errorMessage));
  }
}
