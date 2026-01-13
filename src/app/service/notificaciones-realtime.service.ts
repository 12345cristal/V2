import { Injectable } from '@angular/core';
import { signal } from '@angular/core';
import { AuthService } from '../auth/auth.service';
import { environment } from '../environment/environment';

export interface NotificacionRealtime {
  id?: number;
  mensaje: string;
  tipo: string;   // 'reposicion', 'cita', 'documento', etc.
  fecha: string; // ISO
}

@Injectable({ providedIn: 'root' })
export class NotificacionesRealtimeService {

  private socket: WebSocket | null = null;
  notificaciones = signal<NotificacionRealtime[]>([]);

  constructor(private auth: AuthService) {}

  conectar() {
    const token = this.auth.token;
    if (!token) return;

    // WebSocket temporalmente desactivado - endpoint no implementado en backend
    console.log('WebSocket notificaciones desactivado temporalmente');
    return;

    /* const wsUrl = environment.wsBaseUrl || 'ws://localhost:8000/ws/notificaciones';
    this.socket = new WebSocket(`${wsUrl}?token=${token}`);

    this.socket.onmessage = (event) => {
      try {
        const data: NotificacionRealtime = JSON.parse(event.data);
        this.notificaciones.update((prev) => [data, ...prev]);
      } catch (e) {
        console.error('Error parseando notificación WS', e);
      }
    };

    this.socket.onclose = () => {
      console.warn('WS notificaciones cerrado');
      this.socket = null;
      // opcional: reconectar con backoff
    }; */
  }

  desconectar() {
    this.socket?.close();
    this.socket = null;
  }
}
