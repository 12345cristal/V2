import { Component, OnInit, signal } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ActivatedRoute } from '@angular/router';

import { TerapeutaPacientesService } from '../../services/terapeuta-pacientes.service';
import { NinoResumenTerapeuta } from '../../interfaces/nino-resumen-terapeuta.interface';

@Component({
  selector: 'app-paciente-detalle',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './paciente-detalle.html',
  styleUrls: ['./paciente-detalle.scss']
})
export class PacienteDetalleComponent implements OnInit {

  cargando = signal<boolean>(true);
  paciente = signal<NinoResumenTerapeuta | null>(null);

  constructor(
    private route: ActivatedRoute,
    private pacientesService: TerapeutaPacientesService
  ) {}

  ngOnInit(): void {
    const id = Number(this.route.snapshot.paramMap.get('id'));
    this.cargarDetalle(id);
  }

  cargarDetalle(id: number) {
    this.cargando.set(true);

    this.pacientesService.getDetallePaciente(id).subscribe({
      next: (data) => {
        this.paciente.set(data);
        this.cargando.set(false);
      },
      error: () => {
        this.cargando.set(false);
      }
    });
  }
}
