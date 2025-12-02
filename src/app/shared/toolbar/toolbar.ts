import { Component, EventEmitter, Output } from '@angular/core';
import { NotificacionesIconComponent } from '../../shared/notificaciones/notificaciones-icon/notificaciones-icon';
import { PerfilMenuComponent } from '../../shared/perfil-menu/perfil-menu';

@Component({
  selector: 'app-toolbar',
  standalone: true,
  imports: [
    NotificacionesIconComponent,
    PerfilMenuComponent
  ],
  templateUrl: './toolbar.html',
  styleUrls: ['./toolbar.scss'],
})
export class Toolbar {

  @Output() menuClick = new EventEmitter<void>();

  onMenuClick() {
    this.menuClick.emit();
  }
}
