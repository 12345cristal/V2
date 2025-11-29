// src/app/terapeuta/pages/inicio/inicio-terapeuta.ts

import {
  Component,
  OnInit,
  signal,
  computed
} from '@angular/core';
import { CommonModule } from '@angular/common';
import { MatIconModule } from '@angular/material/icon';

import {
  DashboardTerapeuta,
  SesionDelDia,
  NinoAsignadoHoy,
  NotificacionDashboard,
  TareaRecurso
} from '../../interfaces/inicio-terapeuta.interface';

import { DashboardTerapeutaService } from '../../service/inicio-terapeuta.service';
import { catchError, finalize, of } from 'rxjs';

@Component({
  selector: 'app-inicio-terapeuta',
  standalone: true,
  imports: [CommonModule, MatIconModule],
  templateUrl: './inicio.html',
  styleUrls: ['./inicio.scss']
})
export class InicioTerapeutaComponent implements OnInit {

  dashboard = signal<DashboardTerapeuta | null>(null);
  cargando = signal<boolean>(false);
  error = signal<string | null>(null);

  // 🔹 Derivados para la vista
  sesionesDelDia = computed<SesionDelDia[]>(() =>
    this.dashboard()?.sesionesDelDia ?? []
  );

  ninosAsignadosHoy = computed<NinoAsignadoHoy[]>(() =>
    this.dashboard()?.ninosAsignadosHoy ?? []
  );

  notificaciones = computed<NotificacionDashboard[]>(() =>
    this.dashboard()?.notificaciones ?? []
  );

  tareasPendientes = computed<TareaRecurso[]>(() =>
    this.dashboard()?.tareasPendientes ?? []
  );

  estadisticas = computed(() =>
    this.dashboard()?.estadisticasSemanales ?? null
  );

  constructor(
    private dashboardService: DashboardTerapeutaService
  ) {}

  ngOnInit(): void {
    this.cargarDashboard();
  }

  private cargarDashboard(): void {
    this.cargando.set(true);
    this.error.set(null);

    // 🧪 Para desarrollo usando MOCK:
    this.dashboardService
      .getDashboardMock()
      .pipe(
        finalize(() => this.cargando.set(false)),
        catchError(err => {
          console.error(err);
          this.error.set('No se pudo cargar el dashboard del terapeuta.');
          return of(null);
        })
      )
      .subscribe(data => {
        if (data) {
          this.dashboard.set(data);
        }
      });

    // 🔵 Cuando tengas backend real, cambia a:
    /*
    this.dashboardService
      .getDashboard()
      .pipe(
        finalize(() => this.cargando.set(false)),
        catchError(err => {
          console.error(err);
          this.error.set('No se pudo cargar el dashboard del terapeuta.');
          return of(null);
        })
      )
      .subscribe(data => {
        if (data) {
          this.dashboard.set(data);
        }
      });
    */
  }

  // Helpers UI
  getEstadoClase(estado?: string): string {
    switch (estado) {
      case 'ACTIVO':
        return 'estado-chip activo';
      case 'VACACIONES':
        return 'estado-chip vacaciones';
      case 'INACTIVO':
        return 'estado-chip inactivo';
      default:
        return 'estado-chip';
    }
  }

  getTipoNotificacionIcono(tipo: string): string {
    switch (tipo) {
      case 'reposicion':
        return 'history';          // mat-icon
      case 'cambio-horario':
        return 'schedule';
      case 'documento':
        return 'description';
      case 'alerta':
        return 'warning';
      default:
        return 'notifications';
    }
  }

  getProgresoPorcentaje(completados: number, total: number): number {
    if (!total) return 0;
    return Math.round((completados / total) * 100);
  }

  // Acciones rápidas (por ahora solo log, luego conectas navegación)
  registrarNotaInmediata(): void {
    console.log('Registrar nota inmediata');
  }

  agregarReposicion(): void {
    console.log('Agregar reposición');
  }

  enviarRecurso(): void {
    console.log('Enviar recurso');
  }

  verPacientes(): void {
    console.log('Ver pacientes');
  }

  verHorarios(): void {
    console.log('Ver horarios');
  }
}
