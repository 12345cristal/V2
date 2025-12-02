import { Component, computed } from '@angular/core';
import { Router } from '@angular/router';
import { NotificacionesService } from '../../../service/notificaciones.service';

@Component({
  selector: 'app-notificaciones-icon',
  standalone: true,
  templateUrl: './notificaciones-icon.html',
  styleUrls: ['./notificaciones-icon.scss']
})
export class NotificacionesIconComponent {

  total = computed(() => this.notificacionesService.total);

  constructor(
    private router: Router,
    private notificacionesService: NotificacionesService
  ) {}

  irNotificaciones() {
    this.router.navigate(['/notificaciones']);
  }
}
