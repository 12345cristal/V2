import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { CommonModule } from '@angular/common';
import { MatIconModule } from '@angular/material/icon';

import { Personal, Rol } from '../../../interfaces/personal.interface';
import { PersonalService } from '../../../service/personal.service';
import { NotificationService } from '../../../shared/notification.service';

type Vista = 'tarjetas' | 'tabla' | 'horarios';

@Component({
  selector: 'app-personal-list',
  standalone: true,
  templateUrl: './personal-list.html',
  styleUrls: ['./personal-list.scss'],
  imports: [CommonModule, MatIconModule]
})
export class PersonalListComponent implements OnInit {

  vistaActual: Vista = 'tarjetas';

  personal: Personal[] = [];
  roles: Rol[] = [];

  filtroTexto = '';
  filtroRol: number | 'all' = 'all';
  filtroEstado: 'all' | 'ACTIVO' | 'VACACIONES' | 'INACTIVO' = 'all';

  cargando = false;
  errorCarga = '';

  constructor(
    private personalService: PersonalService,
    private router: Router,
    private notificationService: NotificationService
  ) {}

  ngOnInit(): void {
    this.cargarDatos();
  }

  private cargarDatos(): void {
    this.cargando = true;
    this.errorCarga = '';

    this.personalService.getRoles().subscribe({
      next: roles => {
        console.log('Roles cargados:', roles);
        this.roles = roles;
      },
      error: (err) => {
        console.error('Error al cargar roles:', err);
        console.error('Status:', err.status);
        console.error('URL:', err.url);
        console.error('Message:', err.message);
        this.errorCarga = 'No se pudieron cargar los roles.';
      }
    });

    this.personalService.getPersonal().subscribe({
      next: personas => {
        console.log('Personal cargado:', personas);
        this.personal = personas;
        this.cargando = false;
      },
      error: (err) => {
        console.error('Error al cargar personal:', err);
        console.error('Status:', err.status);
        console.error('URL:', err.url);
        console.error('Message:', err.message);
        console.error('Error body:', err.error);
        this.errorCarga = 'No se pudo cargar el personal: ' + (err.error?.detail || err.message);
        this.cargando = false;
      }
    });
  }

  cambiarVista(vista: Vista): void {
    this.vistaActual = vista;
  }

  onBuscar(valor: string): void {
    this.filtroTexto = valor.toLowerCase().trim();
  }

  onFiltrarRol(valor: string): void {
    this.filtroRol = valor === 'all' ? 'all' : Number(valor);
  }

  onFiltrarEstado(valor: string): void {
    this.filtroEstado = valor as 'all' | 'ACTIVO' | 'VACACIONES' | 'INACTIVO';
  }

  get totalPersonal(): number {
    return this.personal.length;
  }

  get totalTeraputas(): number {
    return this.personal.filter(p =>
      this.obtenerNombreRol(p.id_rol).toLowerCase().includes('terap')
    ).length;
  }

  get personalActivo(): number {
    return this.personal.filter(p => p.estado_laboral === 'ACTIVO').length;
  }

  get personalVacaciones(): number {
    return this.personal.filter(p => p.estado_laboral === 'VACACIONES').length;
  }

  get personalInactivo(): number {
    return this.personal.filter(p => p.estado_laboral === 'INACTIVO').length;
  }

  get ratingPromedio(): number {
    const ratings = this.personal
      .map(p => p.rating ?? 0)
      .filter(r => r > 0);
    if (!ratings.length) return 0;
    const suma = ratings.reduce((a, b) => a + b, 0);
    return +(suma / ratings.length).toFixed(1);
  }

  get personalFiltrado(): Personal[] {
    return this.personal.filter(p => {
      const coincideRol = this.filtroRol === 'all'
        ? true
        : p.id_rol === this.filtroRol;

      const coincideEstado = this.filtroEstado === 'all'
        ? true
        : p.estado_laboral === this.filtroEstado;

      const texto = (p.nombres + ' ' +
        p.apellido_paterno + ' ' +
        (p.apellido_materno ?? '') + ' ' +
        p.especialidad_principal).toLowerCase();

      const coincideTexto = !this.filtroTexto
        ? true
        : texto.includes(this.filtroTexto);

      return coincideRol && coincideEstado && coincideTexto;
    });
  }

  obtenerNombreRol(idRol: number): string {
    const rol = this.roles.find(r => r.id_rol === idRol);
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

  verHorarios(personal: Personal): void {
    this.router.navigate(['/coordinador/personal/horarios', personal.id_personal]);
  }

  cambiarEstado(personal: Personal, nuevoEstado: 'ACTIVO' | 'VACACIONES' | 'INACTIVO'): void {
    if (!personal.id_personal) return;
    
    const estadoTexto = nuevoEstado === 'ACTIVO' ? 'Activo' : nuevoEstado === 'VACACIONES' ? 'Vacaciones' : 'Inactivo';
    const nombreCompleto = `${personal.nombres} ${personal.apellido_paterno}`;
    
    if (!confirm(`¿Estás seguro de cambiar el estado de ${nombreCompleto} a "${estadoTexto}"?`)) {
      return;
    }

    this.cargando = true;
    this.personalService.cambiarEstado(personal.id_personal, nuevoEstado).subscribe({
      next: () => {
        personal.estado_laboral = nuevoEstado;
        this.cargando = false;
        this.notificationService.success(`Estado cambiado a ${estadoTexto} correctamente`);
      },
      error: () => {
        this.errorCarga = 'No se pudo cambiar el estado. Intenta nuevamente.';
        this.cargando = false;
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
