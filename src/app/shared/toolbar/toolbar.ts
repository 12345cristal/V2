import { Component, EventEmitter, Output } from '@angular/core';
import { NotificacionesIconComponent } from '../../shared/notificaciones/notificaciones-icon/notificaciones-icon';

@Component({
  selector: 'app-toolbar',
  standalone: true,
  imports: [
    NotificacionesIconComponent  ],
  templateUrl: './toolbar.html',
  styleUrls: ['./toolbar.scss'],
})
export class Toolbar {

  @Output() menuClick = new EventEmitter<void>();

  onMenuClick() {
    this.menuClick.emit();
  }
}

