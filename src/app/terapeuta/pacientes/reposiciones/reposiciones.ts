import { Component, OnInit, signal, computed } from '@angular/core';
import { CommonModule } from '@angular/common';

import { TerapeutaAgendaService } from '../../../service/terapeuta-agenda.service';
import { ReposicionTerapia } from '../../../interfaces/reposicion-terapia.interface';

@Component({
  selector: 'app-reposiciones',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './reposiciones.html',
  styleUrls: ['./reposiciones.scss']
})
export class ReposicionesComponent implements OnInit {

  cargando = signal<boolean>(true);
  reposiciones = signal<ReposicionTerapia[]>([]);
  mensajeAccion = signal<string | null>(null);
  mensajeError = signal<string | null>(null);
  advertencias = signal<string[]>([]);

  filtroEstado = signal<string | 'TODOS'>('TODOS');

  estadosDisponibles = computed(() => {
    const map = new Map<string, string>();
    this.reposiciones().forEach(r => {
      if (!map.has(r.estadoCodigo)) {
        map.set(r.estadoCodigo, r.estadoDescripcion);
      }
    });
    return Array.from(map.entries()).map(([codigo, descripcion]) => ({ codigo, descripcion }));
  });

  listaFiltrada = computed(() => {
    const estado = this.filtroEstado();
    if (estado === 'TODOS') return this.reposiciones();
    return this.reposiciones().filter(r => r.estadoCodigo === estado);
  });

  constructor(private agendaService: TerapeutaAgendaService) {}

  ngOnInit(): void {
    this.cargar();
  }

  cargar() {
    this.cargando.set(true);
    this.mensajeError.set(null);
    this.mensajeAccion.set(null);
    this.advertencias.set([]);

    this.agendaService.getReposiciones().subscribe({
      next: (resp) => {
        this.reposiciones.set(resp);
        this.cargando.set(false);
      },
      error: () => {
        this.cargando.set(false);
        this.mensajeError.set('No se pudieron cargar las reposiciones.');
      }
    });
  }

  cambiarFiltro(estado: string | 'TODOS') {
    this.filtroEstado.set(estado);
  }

  private manejarAccionResultado(mensaje: string, advertencias?: string[]) {
    this.mensajeAccion.set(mensaje);
    this.advertencias.set(advertencias ?? []);
  }

  aprobar(r: ReposicionTerapia) {
    this.agendaService.aprobarReposicion(r.id).subscribe({
      next: (res) => {
        this.manejarAccionResultado(res.mensaje, res.advertencias);
        this.cargar();
      },
      error: () => {
        this.mensajeError.set('No se pudo aprobar la reposición.');
      }
    });
  }

  rechazar(r: ReposicionTerapia) {
    this.agendaService.rechazarReposicion(r.id).subscribe({
      next: (res) => {
        this.manejarAccionResultado(res.mensaje, res.advertencias);
        this.cargar();
      },
      error: () => {
        this.mensajeError.set('No se pudo rechazar la reposición.');
      }
    });
  }
}
