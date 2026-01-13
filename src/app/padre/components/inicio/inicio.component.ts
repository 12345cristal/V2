import { Component, signal, effect, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { PadreDashboardService } from '../../../service/padre-inicio.service';
import { PadreHijosStateService } from '../../../service/padre-hijos-state.service';
import { DashboardPadre } from '../../../interfaces/inicio_padre.interface';
import { Hijo } from '../../interfaces/hijo.interface';

@Component({
  selector: 'app-inicio-padre',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './inicio.component.html',
  styleUrls: ['./inicio.component.scss'],
})
export class InicioPadreComponent {
  private service = inject(PadreDashboardService);
  private hijosState = inject(PadreHijosStateService);

  hijos = this.hijosState.hijos; // compartido
  hijoSeleccionado = this.hijosState.seleccionadoId; // compartido
  dashboard = signal<DashboardPadre | null>(null);
  cargando = signal(true);
  error = signal<string | null>(null);

  constructor() {
    effect(() => {
      const hijoId = this.hijoSeleccionado();
      if (hijoId) {
        this.cargarDashboard(hijoId);
      }
    });
  }

  cargarDashboard(hijoId: number) {
    this.cargando.set(true);
    this.service.getDashboard(hijoId).subscribe({
      next: (data: DashboardPadre) => {
        this.dashboard.set(data);
        this.cargando.set(false);
        this.error.set(null);
      },
      error: (err: unknown) => {
        console.error('Error al cargar dashboard:', err);
        this.error.set('No se pudo cargar el dashboard');
        this.cargando.set(false);
      }
    });
  }

  seleccionarHijo(id: number) {
    this.hijosState.seleccionar(id);
  }

  calcularPorcentaje(completadas: number, totales: number): number {
    return totales > 0 ? Math.round((completadas / totales) * 100) : 0;
  }
}

