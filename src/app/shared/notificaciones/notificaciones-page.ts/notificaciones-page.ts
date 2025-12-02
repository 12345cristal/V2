import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { NotificacionesService } from '../../../service/notificaciones.service';

@Component({
  selector: 'app-notificaciones-page',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './notificaciones-page.html',
  styleUrls: ['./notificaciones-page.scss']
})
export class NotificacionesPage implements OnInit {

  constructor(public notifService: NotificacionesService) {}

  ngOnInit() {
    const id = Number(localStorage.getItem('usuario_id')) || 1;
    this.notifService.cargarNotificaciones(id);
  }
}
