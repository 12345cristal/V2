// src/app/terapeuta/pages/inicio/inicio-terapeuta.ts

import {
  Component,
  OnInit,
  signal,
  computed
} from '@angular/core';
import { CommonModule } from '@angular/common';
import { MatIconModule } from '@angular/material/icon';
import { FormsModule } from '@angular/forms';
import { Router } from '@angular/router';

import {
  DashboardTerapeuta,
  SesionDelDia,
  NinoAsignadoHoy,
  NotificacionDashboard,
  TareaRecurso
} from '../../interfaces/inicio-terapeuta.interface';

import { DashboardTerapeutaService } from '../../service/inicio-terapeuta.service';
import { RegistroSesionModalComponent } from '../shared/registro-sesion-modal/registro-sesion-modal';
import { catchError, finalize, of } from 'rxjs';

@Component({
  selector: 'app-inicio-terapeuta',
  standalone: true,
  imports: [CommonModule, MatIconModule, FormsModule, RegistroSesionModalComponent],
  templateUrl: './inicio.html',
  styleUrls: ['./inicio-mejorado.scss']
})
export class InicioTerapeutaComponent implements OnInit {

  dashboard = signal<DashboardTerapeuta | null>(null);
  cargando = signal<boolean>(false);
  error = signal<string | null>(null);
  searchQuery = '';
  
  // Control del modal de registro
  mostrarModalRegistro = signal<boolean>(false);
  ninoSeleccionadoId = signal<number | null>(null);
  ninoSeleccionadoNombre = signal<string>('');

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
    private dashboardService: DashboardTerapeutaService,
    private router: Router
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

  // ===== NUEVAS FUNCIONES =====
  
  // Búsqueda global
  onSearch(event: Event): void {
    const query = (event.target as HTMLInputElement).value;
    console.log('Buscando:', query);
    // Aquí implementarás la lógica de búsqueda
  }

  // Notificaciones y mensajes
  abrirNotificaciones(): void {
    console.log('Abrir panel de notificaciones');
    // Implementar modal de notificaciones
  }

  abrirMensajes(): void {
    console.log('Abrir mensajería interna');
    // Implementar navegación a mensajes
  }

  // KPIs
  calcularTasaAsistencia(): number {
    const stats = this.estadisticas();
    if (!stats) return 0;
    const total = stats.totalSesiones;
    const completadas = stats.asistenciasCompletadas;
    return total > 0 ? Math.round((completadas / total) * 100) : 0;
  }

  // Alertas
  tieneAlertasImportantes(): boolean {
    const data = this.dashboard();
    return (data?.resumen.tareasPendientes ?? 0) > 0 || this.tieneAsistenciasSinRegistrar();
  }

  tieneAsistenciasSinRegistrar(): boolean {
    // Lógica para verificar si hay asistencias pendientes
    return false; // Implementar según tu lógica
  }

  // Acciones de niños
  verExpediente(idNino: number): void {
    console.log('Ver expediente del niño:', idNino);
    // Implementar navegación al expediente (solo lectura)
  }

  verHistorial(idNino: number): void {
    console.log('Ver historial terapéutico:', idNino);
    // Implementar navegación al historial
  }

  registrarSesion(idNino: number): void {
    const nino = this.ninosAsignadosHoy().find(n => n.id_nino === idNino);
    if (nino) {
      this.ninoSeleccionadoId.set(idNino);
      this.ninoSeleccionadoNombre.set(nino.nombre);
      this.mostrarModalRegistro.set(true);
    }
  }

  cerrarModalRegistro(): void {
    this.mostrarModalRegistro.set(false);
    this.ninoSeleccionadoId.set(null);
    this.ninoSeleccionadoNombre.set('');
  }

  onSesionRegistrada(sesion: any): void {
    console.log('Sesión registrada exitosamente:', sesion);
    // Aquí conectarás con el servicio para guardar en el backend
    this.cargarDashboard(); // Recargar datos
  }

  // Navegación a otras secciones
  irAReportes(): void {
    this.router.navigate(['/terapeuta/reportes']);
  }

  irAAsistencias(): void {
    this.router.navigate(['/terapeuta/asistencias']);
  }

  irAMensajes(): void {
    this.router.navigate(['/terapeuta/mensajes']);
  }
}

