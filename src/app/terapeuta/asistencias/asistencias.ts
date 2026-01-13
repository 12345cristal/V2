import { Component, Input } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { AsistenciasService } from '../../service/terapeuta/asistencias.service';

@Component({
  standalone: true,
  selector: 'app-asistencias',
  imports: [CommonModule, FormsModule],
  templateUrl: './asistencias.html',
  styleUrls: ['./asistencias.scss'],
})
export class AsistenciasPage {
  @Input() sesionId!: number;

  asistio = true;
  observaciones = '';

  constructor(private asistenciasService: AsistenciasService) {}

  guardar() {
    this.asistenciasService
      .registrarAsistencia({
        sesion_id: this.sesionId,
        asistio: this.asistio,
        observaciones: this.observaciones,
      })
      .subscribe(() => alert('Asistencia registrada'));
  }
}
