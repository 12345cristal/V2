import { Component, OnInit, signal, computed, inject, ChangeDetectionStrategy } from '@angular/core';
import { Router } from '@angular/router';
import { CommonModule } from '@angular/common';
import { MatIconModule } from '@angular/material/icon';

import { Personal, Rol } from '../../../interfaces/personal.interface';
import { PersonalService } from '../../../service/personal.service';
import { NotificationService } from '../../../shared/notification.service';

type Vista = 'tarjetas' | 'tabla';

@Component({
  selector: 'app-personal-list',
  standalone: true,
  templateUrl: './personal-list.html',
  styleUrls: ['./personal-list.scss'],
  imports: [CommonModule, MatIconModule],
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class PersonalListComponent implements OnInit {
  readonly vistaActual = signal<Vista>('tarjetas');
  readonly personal = signal<Personal[]>([]);
  readonly roles = signal<Rol[]>([]);
  readonly filtroTexto = signal('');
  readonly filtroRol = signal<number | 'all'>('all');
  readonly filtroEstado = signal<'all' | 'ACTIVO' | 'VACACIONES' | 'INACTIVO'>('all');
  readonly cargando = signal(false);
  readonly errorCarga = signal('');
  readonly mostrarModalVacaciones = signal(false);
  readonly dateInicio = signal('');
  readonly dateFin = signal('');

  private personalService = inject(PersonalService);
  private router = inject(Router);
  private notificationService = inject(NotificationService);

  ngOnInit(): void {
    this.cargarDatos();
  }

  private cargarDatos(): void {
    this.cargando.set(true);
    this.errorCarga.set('');

    this.personalService.getRoles().subscribe({
      next: roles => {
        console.log('Roles cargados:', roles);
        this.roles.set(roles);
      },
      error: (err) => {
        console.error('Error al cargar roles:', err);
        this.errorCarga.set('No se pudieron cargar los roles.');
      }
    });

    this.personalService.getPersonal().subscribe({
      next: personas => {
        console.log('Personal cargado:', personas);
        this.personal.set(personas);
        this.cargando.set(false);
      },
      error: (err) => {
        console.error('Error al cargar personal:', err);
        this.errorCarga.set('No se pudo cargar el personal: ' + (err.error?.detail || err.message));
        this.cargando.set(false);
      }
    });
  }

  readonly personalFiltrado = computed(() => {
    const personal = this.personal();
    const filtroTexto = this.filtroTexto().toLowerCase().trim();
    const filtroRol = this.filtroRol();
    const filtroEstado = this.filtroEstado();

    return personal.filter(p => {
      const coincideRol = filtroRol === 'all' ? true : p.id_rol === filtroRol;
      const coincideEstado = filtroEstado === 'all' ? true : p.estado_laboral === filtroEstado;
      const texto = (`${p.nombres} ${p.apellido_paterno} ${p.apellido_materno ?? ''} ${p.especialidad_principal}`).toLowerCase();
      const coincideTexto = !filtroTexto ? true : texto.includes(filtroTexto);
      return coincideRol && coincideEstado && coincideTexto;
    });
  });

  readonly totalPersonal = computed(() => this.personal().length);
  readonly totalTeraputas = computed(() =>
    this.personal().filter(p =>
      this.obtenerNombreRol(p.id_rol).toLowerCase().includes('terap')
    ).length
  );
  readonly personalActivo = computed(() => this.personal().filter(p => p.estado_laboral === 'ACTIVO').length);
  readonly personalVacaciones = computed(() => this.personal().filter(p => p.estado_laboral === 'VACACIONES').length);
  readonly personalInactivo = computed(() => this.personal().filter(p => p.estado_laboral === 'INACTIVO').length);
  readonly ratingPromedio = computed(() => {
    const ratings = this.personal()
      .map(p => p.rating ?? 0)
      .filter(r => r > 0);
    if (!ratings.length) return 0;
    const suma = ratings.reduce((a, b) => a + b, 0);
    return +(suma / ratings.length).toFixed(1);
  });

  cambiarVista(vista: Vista): void {
    this.vistaActual.set(vista);
  }

  onBuscar(valor: string): void {
    this.filtroTexto.set(valor.toLowerCase().trim());
  }

  onFiltrarRol(valor: string): void {
    this.filtroRol.set(valor === 'all' ? 'all' : Number(valor));
  }

  onFiltrarEstado(valor: string): void {
    this.filtroEstado.set(valor as 'all' | 'ACTIVO' | 'VACACIONES' | 'INACTIVO');
  }

  obtenerNombreRol(idRol: number): string {
    const rol = this.roles().find(r => r.id_rol === idRol);
    return rol ? rol.nombre_rol : '';
  }

  abrirDetalle(personal: Personal): void {
    this.router.navigate(['/coordinador/personal/detalle', personal.id_personal]);
  }

  editar(personal: Personal): void {
    this.router.navigate(['/coordinador/personal/editar', personal.id_personal]);
  }

  agregar(): void {
    this.router.navigate(['/coordinador/personal/nuevo']);
  }

  abrirModalVacaciones(): void {
    this.mostrarModalVacaciones.set(true);
  }

  cerrarModalVacaciones(): void {
    this.mostrarModalVacaciones.set(false);
    this.dateInicio.set('');
    this.dateFin.set('');
  }

  aplicarVacacionesMasivas(): void {
    const inicio = this.dateInicio();
    const fin = this.dateFin();

    if (!inicio || !fin) {
      this.notificationService.error('Debes seleccionar fechas de inicio y fin');
      return;
    }

    if (new Date(inicio) > new Date(fin)) {
      this.notificationService.error('La fecha de inicio no puede ser mayor que la fecha de fin');
      return;
    }

    const personalActivos = this.personal().filter(p => p.estado_laboral === 'ACTIVO');
    if (!personalActivos.length) {
      this.notificationService.warning('No hay personal activo para aplicar vacaciones');
      return;
    }

    // TODO: Implementar llamada al backend para vacaciones masivas
    this.notificationService.success(`Vacaciones aplicadas a ${personalActivos.length} personal`);
    this.cerrarModalVacaciones();
  }

  cambiarEstado(personal: Personal, nuevoEstado: 'ACTIVO' | 'VACACIONES' | 'INACTIVO'): void {
    if (!personal.id_personal) return;
    
    const estadoTexto = nuevoEstado === 'ACTIVO' ? 'Activo' : nuevoEstado === 'VACACIONES' ? 'Vacaciones' : 'Inactivo';
    const nombreCompleto = `${personal.nombres} ${personal.apellido_paterno}`;
    
    if (!confirm(`¿Estás seguro de cambiar el estado de ${nombreCompleto} a "${estadoTexto}"?`)) {
      return;
    }

    this.cargando.set(true);
    this.personalService.cambiarEstado(personal.id_personal, nuevoEstado).subscribe({
      next: () => {
        personal.estado_laboral = nuevoEstado;
        this.cargando.set(false);
        this.notificationService.success(`Estado cambiado a ${estadoTexto} correctamente`);
      },
      error: () => {
        this.errorCarga.set('No se pudo cambiar el estado. Intenta nuevamente.');
        this.cargando.set(false);
        this.notificationService.error('No se pudo cambiar el estado');
      }
    });
  }

  puedeActivar(personal: Personal): boolean {
    return personal.estado_laboral !== 'ACTIVO';
  }

  puedePonerVacaciones(personal: Personal): boolean {
    return personal.estado_laboral !== 'VACACIONES';
  }

  puedeInactivar(personal: Personal): boolean {
    return personal.estado_laboral !== 'INACTIVO';
  }
}



