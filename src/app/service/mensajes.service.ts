// src/app/service/mensajes.service.ts
import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, BehaviorSubject } from 'rxjs';
import { environment } from '../../environments/environment';
import {
  ChatListaItem,
  MensajeItem,
  ConversacionDetalle,
  CrearConversacionRequest
} from '../interfaces/chat.interface';

@Injectable({ providedIn: 'root' })
export class MensajesService {

  private readonly apiUrl =
    `${environment.apiBaseUrl}/mensajes`;

  private nuevoMensajeSubject =
    new BehaviorSubject<MensajeItem | null>(null);

  nuevoMensaje$ = this.nuevoMensajeSubject.asObservable();

  constructor(private http: HttpClient) {}

  listarChats(ninoId?: number): Observable<ChatListaItem[]> {
    let url = `${this.apiUrl}/chats`;
    if (ninoId) url += `?nino_id=${ninoId}`;
    return this.http.get<ChatListaItem[]>(url);
  }

  obtenerConversacion(id: number): Observable<ConversacionDetalle> {
    return this.http.get<ConversacionDetalle>(
      `${this.apiUrl}/conversacion/${id}`
    );
  }

  listarMensajes(id: number, limit = 50, offset = 0) {
    return this.http.get<MensajeItem[]>(
      `${this.apiUrl}/mensajes/${id}?limit=${limit}&offset=${offset}`
    );
  }

  enviarTexto(id: number, contenido: string) {
    return this.http.post<MensajeItem>(
      `${this.apiUrl}/enviar-texto`,
      { conversacion_id: id, contenido }
    );
  }

  enviarArchivo(id: number, archivo: File) {
    const fd = new FormData();
    fd.append('conversacion_id', id.toString());
    fd.append('archivo', archivo);

    return this.http.post<MensajeItem>(
      `${this.apiUrl}/enviar-archivo`,
      fd
    );
  }

  marcarVisto(id: number) {
    return this.http.post(`${this.apiUrl}/marcar-visto/${id}`, {});
  }

  crearConversacion(req: CrearConversacionRequest) {
    return this.http.post(`${this.apiUrl}/crear-conversacion`, req);
  }

  eliminarMensaje(id: number) {
    return this.http.delete(`${this.apiUrl}/mensaje/${id}`);
  }

  emitirNuevoMensaje(m: MensajeItem): void {
    this.nuevoMensajeSubject.next(m);
  }
  enviarAudio(conversacionId: number, blob: Blob) {
  const formData = new FormData();
  formData.append('conversacion_id', conversacionId.toString());
  formData.append('archivo', blob, `audio_${Date.now()}.webm`);

  return this.http.post<MensajeItem>(
    `${this.apiUrl}/enviar-archivo`,
    formData
  );
}

}
