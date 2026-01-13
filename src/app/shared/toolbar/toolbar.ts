import { Component, EventEmitter, Output, signal } from '@angular/core';
import { CommonModule } from '@angular/common';

import { NotificacionesIconComponent } from '../notificaciones/notificaciones-icon/notificaciones-icon';

@Component({
  selector: 'app-toolbar',
  standalone: true,
  imports: [
    CommonModule,
    NotificacionesIconComponent
  ],
  templateUrl: './toolbar.html',
  styleUrls: ['./toolbar.scss'],
})
export class Toolbar {

  @Output() menuClick = new EventEmitter<void>();

  // controla el panel de notificaciones
  mostrarNotificaciones = signal<boolean>(false);

  onMenuClick() {
    this.menuClick.emit();
  }

  toggleNotificaciones() {
    this.mostrarNotificaciones.update(v => !v);
  }
}
