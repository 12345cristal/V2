import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { CommonModule } from '@angular/common';
import { MatIconModule } from '@angular/material/icon';

import { Personal, Rol } from '../../interfaces/personal.interface';
import { PersonalService } from '../../../service/personal.service';

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

  cargando = false;
  errorCarga = '';

  constructor(
    private personalService: PersonalService,
    private router: Router
  ) {}

  ngOnInit(): void {
    this.cargarDatos();
  }

  private cargarDatos(): void {
    this.cargando = true;
    this.errorCarga = '';

    this.personalService.getRoles().subscribe({
      next: roles => this.roles = roles,
      error: () => this.errorCarga = 'No se pudieron cargar los roles.'
    });

    this.personalService.getPersonal().subscribe({
      next: personas => {
        this.personal = personas;
        this.cargando = false;
      },
      error: () => {
        this.errorCarga = 'No se pudo cargar el personal.';
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

      const texto = (p.nombres + ' ' +
        p.apellido_paterno + ' ' +
        (p.apellido_materno ?? '') + ' ' +
        p.especialidad_principal).toLowerCase();

      const coincideTexto = !this.filtroTexto
        ? true
        : texto.includes(this.filtroTexto);

      return coincideRol && coincideTexto;
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
}
