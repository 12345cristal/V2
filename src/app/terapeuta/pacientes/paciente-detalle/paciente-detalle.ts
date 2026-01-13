import { Component, OnInit, signal } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ActivatedRoute } from '@angular/router';

import { TerapeutaPacientesService } from '../../../service/terapeuta-pacientes.service';
import { NinoResumenTerapeuta } from '../../../interfaces/nino-resumen-terapeuta.interface';

import { BitacoraFormComponent, BitacoraFormPayload } from '../bitacora-form/bitcora-form';
import { BitacoraHistorialComponent } from '../bitacora-historial/bitacora-historial';
import { BitacoraResultado } from '../../../interfaces/bitacora.interface';

@Component({
  selector: 'app-paciente-detalle',
  standalone: true,
  imports: [
    CommonModule,
    BitacoraFormComponent,
    BitacoraHistorialComponent
  ],
  templateUrl: './paciente-detalle.html',
  styleUrls: ['./paciente-detalle.scss']
})
export class PacienteDetalleComponent implements OnInit {

  cargando = signal(true);
  paciente = signal<NinoResumenTerapeuta | null>(null);

  mensajeAccion = signal<string | null>(null);
  advertencias = signal<string[]>([]);
  error = signal<string | null>(null);

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
    this.error.set(null);

    this.pacientesService.getDetallePaciente(id).subscribe({
      next: (data) => {
        this.paciente.set(data);
        this.cargando.set(false);
      },
      error: () => {
        this.cargando.set(false);
        this.error.set('No se pudo cargar la información del paciente.');
      }
    });
  }

  onBitacoraSubmit(payload: BitacoraFormPayload) {
    const p = this.paciente();
    if (!p) return;

    const fd = new FormData();
    Object.entries(payload).forEach(([k, v]) => fd.append(k, String(v)));

    this.mensajeAccion.set(null);
    this.advertencias.set([]);

    this.pacientesService.registrarBitacora(p.id, fd).subscribe({
      next: (resp: BitacoraResultado) => {
        this.mensajeAccion.set(resp.mensaje);
        this.advertencias.set(resp.advertencias ?? []);
      },
      error: () => {
        this.mensajeAccion.set('Ocurrió un error al registrar la bitácora.');
      }
    });
  }
}



