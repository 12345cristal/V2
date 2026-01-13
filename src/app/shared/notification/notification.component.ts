import { Component, OnInit, OnDestroy, signal, computed, inject } from '@angular/core';
import { MatIconModule } from '@angular/material/icon';
import { CommonModule } from '@angular/common';
import { Router } from '@angular/router';
import { Subscription } from 'rxjs';

import { NotificationService, Notification } from '../notification.service';
import { NotificacionesService } from '../../service/notificaciones.service';
import { Notificacion as NotificacionApp } from '../../interfaces/notificacion.interface';

@Component({
  selector: 'app-notification',
  standalone: true,
  imports: [MatIconModule, CommonModule],
  templateUrl: './notification.component.html',
  styleUrls: ['./notification.component.scss']
})
export class NotificationComponent implements OnInit, OnDestroy {
  // Toast temporal
  currentNotification = signal<Notification | null>(null);
  private toastSubscription?: Subscription;
  private timeoutId?: number;

  // Servicios
  private notificationService = inject(NotificationService);
  private service = inject(NotificacionesService);
  private router = inject(Router);

  // Estado
  notificaciones = this.service.notificaciones;
  noLeidas = this.service.noLeidas;
  mostrarPanel = false;
  filtroActual: 'todas' | 'noLeidas' = 'todas';

  // Notificaciones filtradas
  notificacionesFiltradas = computed(() => {
    const todas = this.notificaciones();
    if (this.filtroActual === 'noLeidas') {
      return todas.filter(n => !n.leida);
    }
    return todas;
  });

  ngOnInit(): void {
    // Suscribirse a toasts temporales
    this.toastSubscription = this.notificationService.notification$.subscribe(
      notification => {
        this.currentNotification.set(notification);
        
        if (this.timeoutId) {
          clearTimeout(this.timeoutId);
        }

        this.timeoutId = window.setTimeout(() => {
          this.close();
        }, notification.duration || 3000);
      }
    );

    // Cerrar panel al hacer clic fuera
    document.addEventListener('click', this.handleClickOutside);
  }

  ngOnDestroy(): void {
    this.toastSubscription?.unsubscribe();
    if (this.timeoutId) {
      clearTimeout(this.timeoutId);
    }
    document.removeEventListener('click', this.handleClickOutside);
  }

  private handleClickOutside = (event: MouseEvent) => {
    const target = event.target as HTMLElement;
    if (this.mostrarPanel && !target.closest('.notification-bell-container')) {
      this.mostrarPanel = false;
    }
  };

  close(): void {
    this.currentNotification.set(null);
  }

  togglePanel(): void {
    this.mostrarPanel = !this.mostrarPanel;
  }

  cambiarFiltro(filtro: 'todas' | 'noLeidas'): void {
    this.filtroActual = filtro;
  }

  marcarTodasLeidas(): void {
    const usuarioId = this.service.usuarioId();
    const tipo = this.service.tipoUsuario();
    
    if (usuarioId && tipo) {
      this.service.marcarTodasLeidas(usuarioId, tipo).subscribe({
        next: () => {
          this.notificaciones.update(lista =>
            lista.map(n => ({ ...n, leida: true }))
          );
        }
      });
    }
  }

  seleccionarNotificacion(notificacion: NotificacionApp): void {
    // Marcar como leída
    if (!notificacion.leida) {
      this.service.marcarLeida(notificacion.id).subscribe({
        next: (actualizada) => {
          this.notificaciones.update(lista =>
            lista.map(n => n.id === notificacion.id ? actualizada : n)
          );
        }
      });
    }

    // Navegar según el tipo
    this.navegarSegunTipo(notificacion);
    this.mostrarPanel = false;
  }

  private navegarSegunTipo(notificacion: NotificacionApp): void {
    const metadata = notificacion.metadata;
    const tipo = this.service.tipoUsuario();

    if (!metadata || !tipo) return;

    switch (notificacion.tipo) {
      case 'NUEVA_TAREA':
      case 'NUEVO_RECURSO':
        this.router.navigate([`/${tipo}/tareas`]);
        break;
      case 'SESION_REPROGRAMADA':
      case 'SESION_CANCELADA':
      case 'SESION_COMPLETADA':
        this.router.navigate([`/${tipo}/sesiones`]);
        break;
      case 'PAGO_PROXIMO':
      case 'PAGO_ATRASADO':
        this.router.navigate([`/${tipo}/pagos`]);
        break;
      case 'MODIFICACION_TERAPIA':
      case 'INFORME_DISPONIBLE':
        this.router.navigate([`/${tipo}/historial`]);
        break;
      case 'NUEVO_PACIENTE':
        this.router.navigate(['/terapeuta/pacientes']);
        break;
      case 'NUEVA_JUNTA':
      case 'EVENTO_PROXIMO':
        this.router.navigate(['/terapeuta/calendario']);
        break;
      default:
        // No navegar
        break;
    }
  }

  verTodasNotificaciones(): void {
    const tipo = this.service.tipoUsuario();
    this.router.navigate([`/${tipo}/notificaciones`]);
    this.mostrarPanel = false;
  }

  // Helpers
  obtenerIcono(tipo: string): string {
    return this.service.obtenerIconoNotificacion(tipo);
  }

  obtenerTitulo(tipo: string): string {
    return this.service.obtenerTituloNotificacion(tipo);
  }

  obtenerClaseColor(tipo: string): string {
    return this.service.obtenerClaseColor(tipo);
  }

  calcularTiempoRelativo(fecha: string): string {
    const ahora = new Date();
    const fechaNotif = new Date(fecha);
    const diff = ahora.getTime() - fechaNotif.getTime();

    const minutos = Math.floor(diff / 60000);
    const horas = Math.floor(diff / 3600000);
    const dias = Math.floor(diff / 86400000);

    if (minutos < 1) return 'Ahora';
    if (minutos < 60) return `Hace ${minutos}m`;
    if (horas < 24) return `Hace ${horas}h`;
    if (dias < 7) return `Hace ${dias}d`;
    return fechaNotif.toLocaleDateString('es-ES', { day: '2-digit', month: 'short' });
  }

  trackByNotif(index: number, notif: NotificacionApp): number {
    return notif.id;
  }
}




