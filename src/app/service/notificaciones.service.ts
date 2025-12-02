import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { signal } from '@angular/core';
import { environment } from '../enviroment/environment'; // ✔ importante

@Injectable({
  providedIn: 'root'
})
export class NotificacionesService {

  // Estado reactivo con signals
  notificaciones = signal<any[]>([]);

  // Base URL desde el environment
  private readonly baseUrl = environment.apiBaseUrl;

  constructor(private http: HttpClient) {}

  /**
   * Carga todas las notificaciones de un usuario
   */
  cargarNotificaciones(usuarioId: number) {
    this.http.get<any[]>(`${this.baseUrl}/notificaciones/${usuarioId}`)
      .subscribe({
        next: (res) => this.notificaciones.set(res),
        error: (err) => {
          console.error('Error al cargar notificaciones:', err);
          this.notificaciones.set([]); // evita crasheos
        }
      });
  }

  /**
   * Total de notificaciones
   */
  get total() {
    return this.notificaciones().length;
  }
}
