import { Component, signal } from '@angular/core';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-notificaciones-icon',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './notificaciones-icon.html',
  styleUrls: ['./notificaciones-icon.scss']
})
export class NotificacionesIconComponent {
  tieneNotificaciones = signal<boolean>(true);
}
