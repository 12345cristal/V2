import { Injectable, inject, signal, effect } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from 'src/environments/environment';
import { Notificacion } from '../interfaces/notificacion.interface';

@Injectable({ providedIn: 'root' })
export class NotificacionesService {
  private http = inject(HttpClient);
  private baseUrl = `${environment.apiBaseUrl}/notificaciones`;
  private wsUrl = environment.wsBaseUrl;

  private ws: WebSocket | null = null;
  
  notificaciones = signal<Notificacion[]>([]);
  noLeidas = signal<number>(0);
  
  // Usuario actual (padre o terapeuta)
  usuarioId = signal<number | null>(null);
  tipoUsuario = signal<'padre' | 'terapeuta' | null>(null);

  conectarWebSocket(usuarioId: number, tipo: 'padre' | 'terapeuta') {
    if (this.ws) {
      this.ws.close();
    }

    this.usuarioId.set(usuarioId);
    this.tipoUsuario.set(tipo);

    const wsFullUrl = `${this.wsUrl}/notificaciones/ws/${tipo}/${usuarioId}`;
    this.ws = new WebSocket(wsFullUrl);

    this.ws.onopen = () => {
      console.log('WebSocket conectado');
    };

    this.ws.onmessage = (event) => {
      const notificacion: Notificacion = JSON.parse(event.data);
      
      // Agregar a la lista
      this.notificaciones.update(lista => [notificacion, ...lista]);
      
      // Actualizar contador
      this.actualizarContadorNoLeidas();
      
      // Mostrar notificación del navegador
      this.mostrarNotificacionNavegador(notificacion);
      
      // Reproducir sonido
      this.reproducirSonidoNotificacion();
    };

    this.ws.onerror = (error) => {
      console.error('WebSocket error:', error);
    };

    this.ws.onclose = () => {
      console.log('WebSocket cerrado, reconectando...');
      setTimeout(() => this.conectarWebSocket(usuarioId, tipo), 5000);
    };
  }

  desconectar() {
    if (this.ws) {
      this.ws.close();
      this.ws = null;
    }
  }

  cargarNotificaciones(usuarioId: number, tipo: 'padre' | 'terapeuta') {
    return this.http.get<Notificacion[]>(`${this.baseUrl}/${tipo}/${usuarioId}`).subscribe({
      next: (lista) => {
        this.notificaciones.set(lista);
        this.actualizarContadorNoLeidas();
      }
    });
  }

  getNotificaciones(usuarioId: number, tipo: 'padre' | 'terapeuta', soloNoLeidas: boolean = false): Observable<Notificacion[]> {
    const params = soloNoLeidas ? '?solo_no_leidas=true' : '';
    return this.http.get<Notificacion[]>(`${this.baseUrl}/${tipo}/${usuarioId}${params}`);
  }

  marcarLeida(notificacionId: number): Observable<Notificacion> {
    return this.http.put<Notificacion>(`${this.baseUrl}/${notificacionId}/marcar-leida`, {});
  }

  marcarTodasLeidas(usuarioId: number, tipo: 'padre' | 'terapeuta'): Observable<{ marcadas: number }> {
    return this.http.put<{ marcadas: number }>(`${this.baseUrl}/${tipo}/${usuarioId}/marcar-todas-leidas`, {});
  }

  private actualizarContadorNoLeidas() {
    const count = this.notificaciones().filter(n => !n.leida).length;
    this.noLeidas.set(count);
  }

  private mostrarNotificacionNavegador(notificacion: Notificacion) {
    if ('Notification' in window && Notification.permission === 'granted') {
      const icono = this.obtenerIconoNotificacion(notificacion.tipo);
      new Notification(icono + ' ' + this.obtenerTituloNotificacion(notificacion.tipo), {
        body: notificacion.mensaje,
        icon: '/assets/logo.png',
        badge: '/assets/badge.png',
        tag: notificacion.id.toString()
      });
    }
  }

  private reproducirSonidoNotificacion() {
    const audio = new Audio('/assets/sounds/notification.mp3');
    audio.volume = 0.3;
    audio.play().catch(() => {
      // Silenciar error si no se puede reproducir
    });
  }

  solicitarPermisoNotificaciones() {
    if ('Notification' in window && Notification.permission === 'default') {
      Notification.requestPermission();
    }
  }

  obtenerIconoNotificacion(tipo: string): string {
    const iconos: Record<string, string> = {
      // Padre
      'NUEVA_TAREA': '📝',
      'MODIFICACION_TERAPIA': '🔄',
      'SESION_REPROGRAMADA': '📅',
      'SESION_CANCELADA': '❌',
      'PAGO_PROXIMO': '💳',
      'PAGO_ATRASADO': '⚠️',
      'NUEVO_COMENTARIO': '💬',
      'NUEVO_RECURSO': '📎',
      'SESION_COMPLETADA': '✅',
      'INFORME_DISPONIBLE': '📊',
      // Terapeuta
      'HORARIO_ACTUALIZADO': '⏰',
      'NUEVA_JUNTA': '👥',
      'EVENTO_PROXIMO': '🎯',
      'NUEVO_PACIENTE': '🆕',
      'TAREA_COMPLETADA': '✔️',
      'MENSAJE_COORDINADOR': '📧'
    };
    return iconos[tipo] || '🔔';
  }

  obtenerTituloNotificacion(tipo: string): string {
    const titulos: Record<string, string> = {
      // Padre
      'NUEVA_TAREA': 'Nueva tarea asignada',
      'MODIFICACION_TERAPIA': 'Terapia modificada',
      'SESION_REPROGRAMADA': 'Sesión reprogramada',
      'SESION_CANCELADA': 'Sesión cancelada',
      'PAGO_PROXIMO': 'Pago próximo',
      'PAGO_ATRASADO': 'Pago atrasado',
      'NUEVO_COMENTARIO': 'Nuevo comentario',
      'NUEVO_RECURSO': 'Nuevo recurso disponible',
      'SESION_COMPLETADA': 'Sesión completada',
      'INFORME_DISPONIBLE': 'Informe disponible',
      // Terapeuta
      'HORARIO_ACTUALIZADO': 'Horario actualizado',
      'NUEVA_JUNTA': 'Nueva junta programada',
      'EVENTO_PROXIMO': 'Evento próximo',
      'NUEVO_PACIENTE': 'Nuevo paciente asignado',
      'TAREA_COMPLETADA': 'Tarea completada',
      'MENSAJE_COORDINADOR': 'Mensaje del coordinador'
    };
    return titulos[tipo] || 'Notificación';
  }

  obtenerClaseColor(tipo: string): string {
    const colores: Record<string, string> = {
      'PAGO_ATRASADO': 'danger',
      'SESION_CANCELADA': 'danger',
      'PAGO_PROXIMO': 'warning',
      'NUEVA_TAREA': 'info',
      'NUEVO_RECURSO': 'info',
      'SESION_COMPLETADA': 'success',
      'TAREA_COMPLETADA': 'success',
      'MODIFICACION_TERAPIA': 'warning',
      'SESION_REPROGRAMADA': 'warning',
      'NUEVO_PACIENTE': 'success',
      'HORARIO_ACTUALIZADO': 'info',
      'NUEVA_JUNTA': 'info',
      'EVENTO_PROXIMO': 'warning'
    };
    return colores[tipo] || 'default';
  }
}

