// ninos.ts
import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { Router } from '@angular/router';

import { NinosService } from '../../../service/ninos.service';
import { Nino, EstadoNino } from '../../interfaces/nino.interface';

@Component({
  selector: 'app-ninos',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './ninos.html',
  styleUrls: ['./ninos.scss']
})
export class Ninos implements OnInit {

  ninos: Nino[] = [];
  filtered: Nino[] = [];

  viewMode: 'cards' | 'list' = 'cards';
  searchTerm = '';
  filtroEstado: EstadoNino | 'TODOS' = 'TODOS';

  // stats
  total = 0;
  activos = 0;
  nuevosMes = 0;
  promedioProgreso = 0;

  loading = false;
  error = '';

  constructor(
    private ninosService: NinosService,
    private router: Router
  ) {}

  ngOnInit(): void {
    this.cargarNinos();
  }

  cargarNinos(): void {
    this.loading = true;
    this.error = '';

    this.ninosService.getNinos().subscribe({
      next: (res) => {
        this.ninos = res ?? [];
        this.total = this.ninos.length;
        this.activos = this.ninos.filter(n => n.infoCentro.estado === 'ACTIVO').length;
        this.promedioProgreso = this.calcularPromedioProgreso(this.ninos);

        const mesActual = new Date().getMonth();
        this.nuevosMes = this.ninos.filter(n => {
          const f = new Date(n.infoCentro.fechaIngreso);
          return f.getMonth() === mesActual;
        }).length;

        this.aplicarFiltros();
        this.loading = false;
      },
      error: () => {
        this.error = 'No se pudieron cargar los niños. Intenta nuevamente.';
        this.loading = false;
      }
    });
  }

  private calcularPromedioProgreso(ninos: Nino[]): number {
    const conProgreso = ninos.filter(n => typeof n.progresoGeneral === 'number');
    if (!conProgreso.length) return 0;

    const sum = conProgreso.reduce((acc, n) => acc + (n.progresoGeneral ?? 0), 0);
    return Math.round(sum / conProgreso.length);
  }

  aplicarFiltros(): void {
    const term = this.searchTerm.toLowerCase().trim();

    this.filtered = this.ninos.filter(n => {
      const coincideEstado =
        this.filtroEstado === 'TODOS' ||
        n.infoCentro.estado === this.filtroEstado;

      const nombreCompleto =
        `${n.nombre} ${n.apellidoPaterno} ${n.apellidoMaterno}`.toLowerCase();

      const coincideSearch = !term || nombreCompleto.includes(term);

      return coincideEstado && coincideSearch;
    });
  }

  onSearchChange(): void {
    this.aplicarFiltros();
  }

  cambiarView(mode: 'cards' | 'list'): void {
    this.viewMode = mode;
  }

  // 🔥 CORREGIDAS LAS RUTAS AQUÍ
  irANuevo(): void {
    this.router.navigate(['/coordinador/nino/nuevo']);
  }

  editarNino(nino: Nino): void {
    if (!nino.id) return;
    this.router.navigate(['/coordinador/nino', nino.id, 'editar']);
  }

  verPerfil(nino: Nino): void {
    if (!nino.id) return;
    this.router.navigate(['/coordinador/nino', nino.id]);
  }

  badgeEstado(estado: EstadoNino): string {
    switch (estado) {
      case 'ACTIVO': return 'Activo';
      case 'BAJA_TEMPORAL': return 'Baja temporal';
      case 'INACTIVO': return 'Inactivo';
    }
  }

  classEstado(estado: EstadoNino): string {
    switch (estado) {
      case 'ACTIVO': return 'badge badge-success';
      case 'BAJA_TEMPORAL': return 'badge badge-warning';
      case 'INACTIVO': return 'badge badge-muted';
    }
  }
}
