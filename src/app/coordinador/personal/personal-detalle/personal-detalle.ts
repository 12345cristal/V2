import { Component, OnInit, signal, inject, ChangeDetectionStrategy } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { ActivatedRoute, Router } from '@angular/router';
import { MatIconModule } from '@angular/material/icon';

import { Personal } from '../../../interfaces/personal.interface';
import { PersonalService, DatosCompletosPersonal, NinoAsignado, SesionRegistro } from '../../../service/personal.service';

@Component({
  selector: 'app-personal-detalle',
  standalone: true,
  templateUrl: './personal-detalle.html',
  styleUrls: ['./personal-detalle.scss'],
  imports: [CommonModule, FormsModule, MatIconModule],
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class PersonalDetalleComponent implements OnInit {
  readonly personal = signal<Personal | null>(null);
  readonly datosCompletos = signal<DatosCompletosPersonal | null>(null);
  readonly cargando = signal(true);
  readonly error = signal('');
  readonly tabActiva = signal<'info' | 'horarios' | 'historial'>('info');
  readonly filtroNino = signal<number | null>(null);
  readonly filtroAsistencia = signal<'todos' | 'asistio' | 'falto'>('todos');

  private route = inject(ActivatedRoute);
  private router = inject(Router);
  private personalService = inject(PersonalService);

  ngOnInit(): void {
    const id = Number(this.route.snapshot.paramMap.get('id'));
    
    if (!id) {
      this.error.set('ID de personal no válido');
      this.cargando.set(false);
      return;
    }

    // Cargar información básica del personal
    this.personalService.getPersonalById(id).subscribe({
      next: (p) => {
        this.personal.set(p);
      },
      error: (err) => {
        console.error('Error al cargar personal:', err);
        this.error.set('No se pudo cargar la información del personal');
      }
    });

    // Cargar datos completos (horarios, niños, sesiones)
    this.personalService.getDatosCompletos(id).subscribe({
      next: (datos) => {
        this.datosCompletos.set(datos);
        this.cargando.set(false);
      },
      error: (err) => {
        console.error('Error al cargar datos completos:', err);
        this.cargando.set(false);
      }
    });
  }

  cambiarTab(tab: 'info' | 'horarios' | 'historial'): void {
    this.tabActiva.set(tab);
  }

  obtenerSesionesFiltradas(): SesionRegistro[] {
    const datos = this.datosCompletos();
    if (!datos) return [];

    let sesiones = datos.sesiones;

    // Filtrar por niño
    const filtroNino = this.filtroNino();
    if (filtroNino) {
      sesiones = sesiones.filter(s => s.id_nino === filtroNino);
    }

    // Filtrar por asistencia
    const filtroAsist = this.filtroAsistencia();
    if (filtroAsist === 'asistio') {
      sesiones = sesiones.filter(s => s.asistio);
    } else if (filtroAsist === 'falto') {
      sesiones = sesiones.filter(s => !s.asistio);
    }

    return sesiones;
  }

  organizarHorariosPorDia(): { [dia: string]: any[] } {
    const datos = this.datosCompletos();
    if (!datos) return {};

    const diasOrdenados = ['LUNES', 'MARTES', 'MIERCOLES', 'JUEVES', 'VIERNES', 'SABADO', 'DOMINGO'];
    const horariosPorDia: { [dia: string]: any[] } = {};

    diasOrdenados.forEach(dia => {
      horariosPorDia[dia] = datos.horarios
        .filter((h: any) => h.dia_semana === dia)
        .sort((a: any, b: any) => a.hora_inicio.localeCompare(b.hora_inicio));
    });

    return horariosPorDia;
  }

  volver(): void {
    this.router.navigate(['/coordinador/personal']);
  }

  editar(): void {
    const p = this.personal();
    if (!p) return;
    this.router.navigate(['/coordinador/personal/editar', p.id_personal]);
  }

  verHorarios(): void {
    const p = this.personal();
    if (!p) return;
    this.router.navigate(['/coordinador/personal/horarios', p.id_personal]);
  }

  calcularAnosExperiencia(): number {
    const p = this.personal();
    if (!p || !p.fecha_ingreso) return 0;
    const hoy = new Date();
    const ingreso = new Date(p.fecha_ingreso);
    return hoy.getFullYear() - ingreso.getFullYear();
  }

  obtenerEstadoBadgeClass(): string {
    const p = this.personal();
    if (!p) return 'inactivo';
    const estado = p.estado_laboral?.toLowerCase() || 'inactivo';
    switch (estado) {
      case 'activo':
        return 'activo';
      case 'vacaciones':
        return 'vacaciones';
      case 'inactivo':
        return 'inactivo';
      case 'licencia':
        return 'licencia';
      default:
        return 'inactivo';
    }
  }
}
