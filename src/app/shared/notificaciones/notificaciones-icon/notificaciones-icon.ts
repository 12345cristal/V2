import { Component, OnInit, OnDestroy, computed } from '@angular/core';
import { Router } from '@angular/router';
import { NotificacionesService } from '../../../service/notificaciones.service';
import { NotificacionesRealtimeService } from '../../../service/notificaciones-realtime.service';

@Component({
  selector: 'app-notificaciones-icon',
  standalone: true,
  templateUrl: './notificaciones-icon.html',
  styleUrls: ['./notificaciones-icon.scss']
})
export class NotificacionesIconComponent implements OnInit, OnDestroy {

  // Total de notificaciones combinando servicio normal y realtime
  total = computed(() => 
    (this.notificacionesService.total ?? 0) + this.realtime.notificaciones().length
  );

  constructor(
    private router: Router,
    private notificacionesService: NotificacionesService,
    private realtime: NotificacionesRealtimeService
  ) {}

  // Navegar a la página de notificaciones
  irNotificaciones(): void {
    this.router.navigate(['/notificaciones']);
  }

  ngOnInit(): void {
    // Conectar servicio realtime
    this.realtime.conectar();
  }

  ngOnDestroy(): void {
    // Desconectar servicio realtime
    this.realtime.desconectar();
  }
}
