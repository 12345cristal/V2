import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { AuditoriaService } from '../../service/auditoria.service';
import { RegistroAuditoria } from '../../interfaces/auditoria.interface';

@Component({
  selector: 'app-auditoria',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './auditoria.html',
  styleUrls: ['./auditoria.scss']
})
export class AuditoriaComponent {

  filtros = {
    fechaDesde: '',
    fechaHasta: '',
    usuario: '',
    modulo: '',
    accion: ''
  };

  registros: RegistroAuditoria[] = [];
  cargando = false;
  error = '';

  constructor(private auditoriaService: AuditoriaService) {}

  buscar() {
    this.cargando = true;
    this.error = '';
    this.auditoriaService.buscar(this.filtros).subscribe({
      next: res => {
        this.registros = res;
        this.cargando = false;
      },
      error: err => {
        console.error(err);
        this.error = 'Error al consultar auditoría.';
        this.cargando = false;
      }
    });
  }
}

