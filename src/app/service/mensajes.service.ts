import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, BehaviorSubject } from 'rxjs';
import { environment } from '../../environments/environment';
import { ChatListaItem, MensajeItem, ConversacionDetalle, CrearConversacionRequest } from '../interfaces/chat.interface';

@Injectable({
  providedIn: 'root'
})
export class MensajesService {
  private apiUrl = `${environment.apiUrl}/mensajes`;
  
  // Observables para actualizaciones en tiempo real (WebSocket)
  private nuevoMensajeSubject = new BehaviorSubject<MensajeItem | null>(null);
  public nuevoMensaje$ = this.nuevoMensajeSubject.asObservable();

  constructor(private http: HttpClient) {}

  /**
   * Obtiene lista de conversaciones del usuario
   */
  listarChats(ninoId?: number): Observable<ChatListaItem[]> {
    let url = `${this.apiUrl}/chats`;
    if (ninoId) {
      url += `?nino_id=${ninoId}`;
    }
    return this.http.get<ChatListaItem[]>(url);
  }

  /**
   * Obtiene detalles de una conversación
   */
  obtenerConversacion(conversacionId: number): Observable<ConversacionDetalle> {
    return this.http.get<ConversacionDetalle>(
      `${this.apiUrl}/conversacion/${conversacionId}`
    );
  }

  /**
   * Obtiene mensajes de una conversación
   */
  listarMensajes(
    conversacionId: number,
    limit: number = 50,
    offset: number = 0
  ): Observable<MensajeItem[]> {
    return this.http.get<MensajeItem[]>(
      `${this.apiUrl}/mensajes/${conversacionId}?limit=${limit}&offset=${offset}`
    );
  }

  /**
   * Envía un mensaje de texto
   */
  enviarTexto(conversacionId: number, contenido: string): Observable<MensajeItem> {
    return this.http.post<MensajeItem>(`${this.apiUrl}/enviar-texto`, {
      conversacion_id: conversacionId,
      contenido
    });
  }

  /**
   * Envía un archivo o audio
   */
  enviarArchivo(conversacionId: number, archivo: File): Observable<MensajeItem> {
    const formData = new FormData();
    formData.append('conversacion_id', conversacionId.toString());
    formData.append('archivo', archivo);

    return this.http.post<MensajeItem>(
      `${this.apiUrl}/enviar-archivo`,
      formData
    );
  }

  /**
   * Envía audio grabado
   */
  enviarAudio(conversacionId: number, blob: Blob): Observable<MensajeItem> {
    const formData = new FormData();
    formData.append('conversacion_id', conversacionId.toString());
    formData.append('archivo', blob, `audio_${Date.now()}.webm`);

    return this.http.post<MensajeItem>(
      `${this.apiUrl}/enviar-archivo`,
      formData
    );
  }

  /**
   * Marca una conversación como vista
   */
  marcarVisto(conversacionId: number): Observable<any> {
    return this.http.post(
      `${this.apiUrl}/marcar-visto/${conversacionId}`,
      {}
    );
  }

  /**
   * Crea una nueva conversación
   */
  crearConversacion(req: CrearConversacionRequest): Observable<any> {
    return this.http.post(`${this.apiUrl}/crear-conversacion`, req);
  }

  /**
   * Elimina un mensaje
   */
  eliminarMensaje(mensajeId: number): Observable<any> {
    return this.http.delete(`${this.apiUrl}/mensaje/${mensajeId}`);
  }

  /**
   * Emite un nuevo mensaje (para WebSocket)
   */
  emitirNuevoMensaje(mensaje: MensajeItem): void {
    this.nuevoMensajeSubject.next(mensaje);
  }
}




