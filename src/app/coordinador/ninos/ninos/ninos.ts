// ninos.ts
import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { Router } from '@angular/router';

import { NinosService } from '../../../service/ninos.service';
import { Nino, EstadoNino } from '../../../interfaces/nino.interface';

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
    this.cargarEstadisticas();
    this.cargarNinos();
  }

  cargarEstadisticas(): void {
    // Cargar estadísticas generales (sin filtros)
    this.ninosService.getNinos({ pageSize: 100 }).subscribe({
      next: (res) => {
        this.ninos = res ?? [];
        this.total = this.ninos.length;
        this.activos = this.ninos.filter(n => n.infoCentro.estado === 'ACTIVO').length;
        this.promedioProgreso = this.calcularPromedioProgreso(this.ninos);

        const mesActual = new Date().getMonth();
        this.nuevosMes = this.ninos.filter(n => {
          if (!n.infoCentro.fechaIngreso) return false;
          const f = new Date(n.infoCentro.fechaIngreso);
          return f.getMonth() === mesActual;
        }).length;
      },
      error: () => {
        // Las estadísticas no son críticas, continuamos
      }
    });
  }

  cargarNinos(): void {
    this.loading = true;
    this.error = '';

    // Pasar filtros al servicio
    const options = {
      search: this.searchTerm || undefined,
      estado: this.filtroEstado,
      pageSize: 100
    };

    this.ninosService.getNinos(options).subscribe({
      next: (res) => {
        this.filtered = res ?? [];
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
    // Ahora los filtros se aplican en el backend
    this.cargarNinos();
  }

  onSearchChange(): void {
    // Recargar con búsqueda
    this.cargarNinos();
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
    this.router.navigate(['/coordinador/nino', nino.id, 'perfil']);
  }

  badgeEstado(estado: EstadoNino): string {
    switch (estado) {
      case 'ACTIVO': return 'Activo';
      case 'INACTIVO': return 'Inactivo';
    }
  }

  classEstado(estado: EstadoNino): string {
    switch (estado) {
      case 'ACTIVO': return 'badge badge-success';
      case 'INACTIVO': return 'badge badge-muted';
    }
  }

  cambiarEstado(nino: Nino, nuevoEstado: EstadoNino): void {
    if (!nino.id) return;
    
    const estadoTexto = this.badgeEstado(nuevoEstado);
    const nombreCompleto = `${nino.nombre} ${nino.apellidoPaterno}`;
    
    if (!confirm(`¿Estás seguro de cambiar el estado de ${nombreCompleto} a "${estadoTexto}"?`)) {
      return;
    }

    this.loading = true;
    this.ninosService.cambiarEstado(nino.id, nuevoEstado).subscribe({
      next: () => {
        // Actualizar estado localmente
        nino.infoCentro.estado = nuevoEstado;
        
        // Recargar estadísticas y lista filtrada
        this.cargarEstadisticas();
        this.cargarNinos();
        
        this.loading = false;
      },
      error: () => {
        this.error = 'No se pudo cambiar el estado. Intenta nuevamente.';
        this.loading = false;
      }
    });
  }

  puedeActivar(nino: Nino): boolean {
    return nino.infoCentro.estado !== 'ACTIVO';
  }

  puedeInactivar(nino: Nino): boolean {
    return nino.infoCentro.estado !== 'INACTIVO';
  }
}



