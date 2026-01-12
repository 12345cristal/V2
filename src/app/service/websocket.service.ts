import { Injectable, signal } from '@angular/core';
import { BehaviorSubject } from 'rxjs';
import { AuthService } from '../auth/auth.service';
import { environment } from '../environment/environment';

interface WebSocketMensaje {
  tipo: string;
  contenido?: string;
  usuario_id?: number;
  usuario_nombre?: string;
  usuario_rol?: string;
  id?: number;
  conversacion_id?: number;
  emisor_id?: number;
  tipo_mensaje?: string;
  created_at?: string;
  senderNombre?: string;
  senderRol?: string;
  archivoUrl?: string | null;
  archivoNombre?: string | null;
  valor?: boolean;
}

@Injectable({ providedIn: 'root' })
export class WebsocketService {

  private ws: WebSocket | null = null;
  private conversacionIdActual: number | null = null;

  // ============================
  // SIGNALS / OBSERVABLES
  // ============================
  private conectadoSignal = signal<boolean>(false);
  conectado = this.conectadoSignal.asReadonly();

  private nuevoMensajeSubject = new BehaviorSubject<any>(null);
  nuevoMensaje$ = this.nuevoMensajeSubject.asObservable();

  private escribiendoSubject = new BehaviorSubject<Map<number, string>>(new Map());
  usuarioEscribiendo$ = this.escribiendoSubject.asObservable();

  private usuariosConectadosSubject = new BehaviorSubject<Set<number>>(new Set());
  usuariosConectados$ = this.usuariosConectadosSubject.asObservable();

  // ============================
  // RECONEXIÓN
  // ============================
  private reconnectIntentos = 0;
  private readonly maxReconnect = 5;
  private readonly baseDelay = 3000;
  private reconnectTimer: any = null;

  private typingTimer: any = null;

  constructor(private authService: AuthService) {}

  // ============================
  // CONECTAR
  // ============================
  conectar(conversacionId: number): Promise<void> {
    return new Promise((resolve, reject) => {
      const token = this.authService.obtenerToken();
      if (!token) {
        reject('Token no disponible');
        return;
      }

      const wsBase = environment.wsBaseUrl ?? 'ws://localhost:8000';
      const url = `${wsBase}/ws/conversacion/${conversacionId}?token=${token}`;

      this.ws = new WebSocket(url);
      this.conversacionIdActual = conversacionId;
      this.reconnectIntentos = 0;

      this.ws.onopen = () => {
        console.log('✅ WebSocket conectado');
        this.conectadoSignal.set(true);
        resolve();
      };

      this.ws.onmessage = e => {
        const data: WebSocketMensaje = JSON.parse(e.data);
        this.procesarMensaje(data);
      };

      this.ws.onerror = err => {
        console.error('❌ WebSocket error', err);
        this.conectadoSignal.set(false);
        reject(err);
      };

      this.ws.onclose = () => {
        console.warn('⚠️ WebSocket cerrado');
        this.conectadoSignal.set(false);
        this.reintentar();
      };
    });
  }

  // ============================
  // DESCONECTAR
  // ============================
  desconectar(): void {
    if (this.ws) {
      this.ws.close();
      this.ws = null;
      this.conectadoSignal.set(false);
      this.conversacionIdActual = null;
    }

    if (this.reconnectTimer) {
      clearTimeout(this.reconnectTimer);
      this.reconnectTimer = null;
    }
  }

  // ============================
  // ENVIAR MENSAJE
  // ============================
  enviarMensaje(contenido: string): void {
    if (!this.ws || this.ws.readyState !== WebSocket.OPEN) return;

    this.ws.send(JSON.stringify({
      tipo: 'mensaje',
      contenido
    }));
  }

  // ============================
  // ESCRIBIENDO
  // ============================
  notificarEscribiendo(): void {
    if (!this.ws || this.ws.readyState !== WebSocket.OPEN) return;

    this.ws.send(JSON.stringify({ tipo: 'escribiendo', valor: true }));

    clearTimeout(this.typingTimer);
    this.typingTimer = setTimeout(() => {
      this.ws?.send(JSON.stringify({ tipo: 'escribiendo', valor: false }));
    }, 2000);
  }

  // ============================
  // ARCHIVOS
  // ============================
  enviarArchivo(url: string, nombre: string, tipo: 'ARCHIVO' | 'AUDIO'): void {
    if (!this.ws || this.ws.readyState !== WebSocket.OPEN) return;

    this.ws.send(JSON.stringify({
      tipo: 'archivo',
      archivoUrl: url,
      archivoNombre: nombre,
      tipoArchivo: tipo
    }));
  }

  // ============================
  // PROCESAR MENSAJES
  // ============================
  private procesarMensaje(data: WebSocketMensaje): void {
    switch (data.tipo) {

      case 'nuevo_mensaje':
        this.nuevoMensajeSubject.next({
          id: data.id,
          conversacionId: data.conversacion_id,
          emisorId: data.emisor_id,
          contenido: data.contenido,
          tipo: data.tipo_mensaje,
          createdAt: data.created_at,
          senderNombre: data.senderNombre,
          senderRol: data.senderRol,
          archivoUrl: data.archivoUrl,
          archivoNombre: data.archivoNombre
        });
        break;

      case 'usuario_escribiendo':
        this.escribiendoSubject.next(
          new Map(this.escribiendoSubject.value)
            .set(data.usuario_id!, data.usuario_nombre!)
        );
        break;

      case 'usuario_dejo_escribir':
        const map = new Map(this.escribiendoSubject.value);
        map.delete(data.usuario_id!);
        this.escribiendoSubject.next(map);
        break;

      case 'usuario_conectado':
        const on = new Set(this.usuariosConectadosSubject.value);
        on.add(data.usuario_id!);
        this.usuariosConectadosSubject.next(on);
        break;

      case 'usuario_desconectado':
        const off = new Set(this.usuariosConectadosSubject.value);
        off.delete(data.usuario_id!);
        this.usuariosConectadosSubject.next(off);
        break;
    }
  }

  // ============================
  // REINTENTAR CONEXIÓN
  // ============================
  private reintentar(): void {
    if (!this.conversacionIdActual) return;
    if (this.reconnectIntentos >= this.maxReconnect) return;

    this.reconnectIntentos++;
    const delay = this.baseDelay * this.reconnectIntentos;

    this.reconnectTimer = setTimeout(() => {
      this.conectar(this.conversacionIdActual!).catch(() => this.reintentar());
    }, delay);
  }

  // ============================
  // ESTADO
  // ============================
  estaConectado(): boolean {
    return this.conectadoSignal() && this.ws?.readyState === WebSocket.OPEN;
  }
}
