import { Component, OnInit, signal } from '@angular/core';
import { CommonModule } from '@angular/common';

import { TerapeutaAgendaService } from '../../services/terapeuta-agenda.service';
import { ReposicionTerapia } from '../../interfaces/reposicion-terapia.interface';

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
  filtroEstado = signal<'TODAS' | 'PENDIENTE' | 'APROBADA' | 'RECHAZADA'>('PENDIENTE');

  constructor(private agendaService: TerapeutaAgendaService) {}

  ngOnInit(): void {
    this.cargar();
  }

  cargar() {
    this.cargando.set(true);

    this.agendaService.getReposiciones().subscribe({
      next: (resp) => {
        this.reposiciones.set(resp);
        this.cargando.set(false);
      },
      error: () => this.cargando.set(false)
    });
  }

  cambiarFiltro(estado: 'TODAS' | 'PENDIENTE' | 'APROBADA' | 'RECHAZADA') {
    this.filtroEstado.set(estado);
  }

  listaFiltrada() {
    if (this.filtroEstado() === 'TODAS') return this.reposiciones();
    return this.reposiciones().filter(r => r.estado === this.filtroEstado());
  }
}
