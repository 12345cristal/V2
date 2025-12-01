// src/app/padres/pages/inicio-padre/inicio-padre.component.ts

import { Component, OnInit, computed, signal } from '@angular/core';
import { CommonModule } from '@angular/common';

import {
  ActividadPendiente,
  InicioPadreResumen,
  TerapiaDelDia
} from '../../interfaces/inicio-padre.interface';

import { InicioPadreService } from '../../service/inicio-padre.service';

@Component({
  selector: 'app-inicio-padre',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './inicio.html',
  styleUrls: ['./inicio.scss']
})
export class InicioPadreComponent implements OnInit {

  // Estado principal
  private resumenInterno = signal<InicioPadreResumen | null>(null);

  // Estado UI
  cargando = signal<boolean>(false);
  error = signal<string | null>(null);

  // Derivados
  nino = computed(() => this.resumenInterno()?.nino ?? null);
  terapiaDeHoy = computed<TerapiaDelDia | null>(
    () => this.resumenInterno()?.terapiaDeHoy ?? null
  );
  actividadesPendientes = computed<ActividadPendiente[]>(
    () => this.resumenInterno()?.actividadesPendientes ?? []
  );
  mensajeDelDia = computed(() => this.resumenInterno()?.mensajeDelDia ?? null);

  constructor(private inicioService: InicioPadreService) {}

  ngOnInit(): void {
    this.cargarInicio();
  }

  cargarInicio(): void {
    this.cargando.set(true);
    this.error.set(null);

    this.inicioService.obtenerResumenInicio().subscribe({
      next: (resumen) => {
        this.resumenInterno.set(resumen);
        this.cargando.set(false);
      },
      error: () => {
        // En producción puedes leer mensaje real del backend
        this.error.set('Ocurrió un problema al cargar la información de hoy.');
        this.cargando.set(false);
      }
    });
  }

  obtenerEtiquetaEstadoTerapia(estado: string): string {
    if (estado === 'POR_INICIAR') return 'Por iniciar';
    if (estado === 'EN_CURSO') return 'En curso';
    if (estado === 'FINALIZADA') return 'Finalizada';
    return 'Sin estado';
  }

  obtenerClaseEstadoTerapia(estado: string): string {
    if (estado === 'POR_INICIAR') return 'badge badge-warning';
    if (estado === 'EN_CURSO') return 'badge badge-success';
    if (estado === 'FINALIZADA') return 'badge badge-muted';
    return 'badge';
  }

  obtenerEtiquetaTipoActividad(tipo: string): string {
    if (tipo === 'TAREA_CASA') return 'Tarea en casa';
    if (tipo === 'DOCUMENTO') return 'Documento';
    if (tipo === 'CUESTIONARIO') return 'Cuestionario';
    return 'Actividad';
  }

  obtenerClasePrioridad(prioridad: string): string {
    if (prioridad === 'ALTA') return 'pill pill-danger';
    if (prioridad === 'MEDIA') return 'pill pill-warning';
    return 'pill pill-soft';
  }
}
