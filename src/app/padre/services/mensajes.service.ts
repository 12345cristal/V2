import { Injectable } from '@angular/core';
import { HttpClient, HttpErrorResponse, HttpParams } from '@angular/common/http';
import { Observable, throwError } from 'rxjs';
import { catchError, map } from 'rxjs/operators';
import { environment } from '../../enviroment/environment';
import { IChat, IMensaje, ITipoChat } from '../interfaces/mensajes.interface';
import { IResponse, IResponsePaginado } from '../interfaces/shared.interface';

/**
 * Servicio para la gestión de mensajería
 * Proporciona métodos para chats y mensajes
 */
@Injectable({
  providedIn: 'root'
})
export class MensajesService {
  private readonly baseUrl = `${environment.apiBaseUrl}/mensajes`;

  constructor(private http: HttpClient) {}

  /**
   * Obtiene la lista de chats del usuario
   * @param usuarioId ID del usuario
   * @param filtros Filtros opcionales
   * @returns Observable con la lista de chats
   */
  getChats(
    usuarioId: number,
    filtros?: {
      tipo?: ITipoChat;
      activos?: boolean;
      archivados?: boolean;
    }
  ): Observable<IChat[]> {
    let params = new HttpParams().set('usuarioId', usuarioId.toString());

    if (filtros) {
      if (filtros.tipo) params = params.set('tipo', filtros.tipo);
      if (filtros.activos !== undefined) params = params.set('activos', filtros.activos.toString());
      if (filtros.archivados !== undefined) params = params.set('archivados', filtros.archivados.toString());
    }

    return this.http.get<IResponse<IChat[]>>(`${this.baseUrl}/chats`, { params })
      .pipe(
        map(response => response.data || []),
        catchError(this.handleError)
      );
  }

  /**
   * Obtiene un chat por su ID
   * @param chatId ID del chat
   * @returns Observable con el chat
   */
  getChat(chatId: number): Observable<IChat> {
    return this.http.get<IResponse<IChat>>(`${this.baseUrl}/chats/${chatId}`)
      .pipe(
        map(response => response.data!),
        catchError(this.handleError)
      );
  }

  /**
   * Crea un nuevo chat
   * @param data Datos del chat
   * @returns Observable con el chat creado
   */
  crearChat(data: {
    tipo: ITipoChat;
    participantesIds: number[];
    titulo?: string;
    ninoRelacionadoId?: number;
  }): Observable<IChat> {
    return this.http.post<IResponse<IChat>>(`${this.baseUrl}/chats`, data)
      .pipe(
        map(response => response.data!),
        catchError(this.handleError)
      );
  }

  /**
   * Obtiene los mensajes de un chat
   * @param chatId ID del chat
   * @param page Número de página
   * @param pageSize Tamaño de página
   * @returns Observable con los mensajes paginados
   */
  getMensajes(
    chatId: number,
    page: number = 1,
    pageSize: number = 50
  ): Observable<IResponsePaginado<IMensaje>> {
    const params = new HttpParams()
      .set('page', page.toString())
      .set('pageSize', pageSize.toString());

    return this.http.get<IResponsePaginado<IMensaje>>(
      `${this.baseUrl}/chats/${chatId}/mensajes`,
      { params }
    ).pipe(catchError(this.handleError));
  }

  /**
   * Envía un mensaje
   * @param chatId ID del chat
   * @param contenido Contenido del mensaje
   * @param adjuntos Archivos adjuntos (opcional)
   * @param respondidoAId ID del mensaje al que se responde (opcional)
   * @returns Observable con el mensaje enviado
   */
  enviarMensaje(
    chatId: number,
    contenido: string,
    adjuntos?: File[],
    respondidoAId?: number
  ): Observable<IMensaje> {
    const formData = new FormData();
    formData.append('chatId', chatId.toString());
    formData.append('contenido', contenido);
    if (respondidoAId) formData.append('respondidoAId', respondidoAId.toString());
    
    if (adjuntos && adjuntos.length > 0) {
      adjuntos.forEach((archivo, index) => {
        formData.append(`adjuntos[${index}]`, archivo);
      });
    }

    return this.http.post<IResponse<IMensaje>>(this.baseUrl, formData)
      .pipe(
        map(response => response.data!),
        catchError(this.handleError)
      );
  }

  /**
   * Edita un mensaje
   * @param mensajeId ID del mensaje
   * @param nuevoContenido Nuevo contenido
   * @returns Observable con el mensaje actualizado
   */
  editarMensaje(mensajeId: number, nuevoContenido: string): Observable<IMensaje> {
    return this.http.put<IResponse<IMensaje>>(
      `${this.baseUrl}/${mensajeId}`,
      { contenido: nuevoContenido }
    ).pipe(
      map(response => response.data!),
      catchError(this.handleError)
    );
  }

  /**
   * Elimina un mensaje
   * @param mensajeId ID del mensaje
   * @param paraTodos Si es true, elimina para todos los participantes
   * @returns Observable con la confirmación
   */
  eliminarMensaje(mensajeId: number, paraTodos: boolean = false): Observable<void> {
    return this.http.delete<IResponse<void>>(
      `${this.baseUrl}/${mensajeId}`,
      { params: new HttpParams().set('paraTodos', paraTodos.toString()) }
    ).pipe(
      map(() => undefined),
      catchError(this.handleError)
    );
  }

  /**
   * Marca los mensajes de un chat como leídos
   * @param chatId ID del chat
   * @returns Observable con la confirmación
   */
  marcarComoLeidos(chatId: number): Observable<void> {
    return this.http.patch<IResponse<void>>(
      `${this.baseUrl}/chats/${chatId}/marcar-leidos`,
      {}
    ).pipe(
      map(() => undefined),
      catchError(this.handleError)
    );
  }

  /**
   * Silencia las notificaciones de un chat
   * @param chatId ID del chat
   * @param silenciar Si es true silencia, si es false activa notificaciones
   * @returns Observable con el chat actualizado
   */
  silenciarChat(chatId: number, silenciar: boolean): Observable<IChat> {
    return this.http.patch<IResponse<IChat>>(
      `${this.baseUrl}/chats/${chatId}/silenciar`,
      { silenciado: silenciar }
    ).pipe(
      map(response => response.data!),
      catchError(this.handleError)
    );
  }

  /**
   * Archiva un chat
   * @param chatId ID del chat
   * @param archivar Si es true archiva, si es false desarchia
   * @returns Observable con el chat actualizado
   */
  archivarChat(chatId: number, archivar: boolean): Observable<IChat> {
    return this.http.patch<IResponse<IChat>>(
      `${this.baseUrl}/chats/${chatId}/archivar`,
      { archivado: archivar }
    ).pipe(
      map(response => response.data!),
      catchError(this.handleError)
    );
  }

  /**
   * Busca mensajes en un chat
   * @param chatId ID del chat
   * @param termino Término de búsqueda
   * @returns Observable con los mensajes encontrados
   */
  buscarMensajes(chatId: number, termino: string): Observable<IMensaje[]> {
    const params = new HttpParams()
      .set('chatId', chatId.toString())
      .set('q', termino);

    return this.http.get<IResponse<IMensaje[]>>(`${this.baseUrl}/buscar`, { params })
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
    
    console.error('Error en MensajesService:', errorMessage);
    return throwError(() => new Error(errorMessage));
  }
}
