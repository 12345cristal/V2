import { Component, Input } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { ReportesService } from '../../service/terapeuta/reportes.service';

@Component({
  standalone: true,
  selector: 'app-reportes',
  imports: [CommonModule, FormsModule],
  templateUrl: './reportes.html',
  styleUrls: ['./reportes.scss'],
})
export class ReportesPage {
  @Input() ninoId!: number;

  observaciones = '';

  constructor(private reportesService: ReportesService) {}

  guardar() {
    this.reportesService
      .crearReporteSesion({
        nino_id: this.ninoId,
        sesion_id: 0,
        observaciones: this.observaciones,
      })
      .subscribe(() => alert('Reporte guardado'));
  }
}
