import { Component, OnInit, signal } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterLink } from '@angular/router';

import { TerapeutaPacientesService } from '../../services/terapeuta-pacientes.service';
import { NinoResumenTerapeuta } from '../../interfaces/nino-resumen-terapeuta.interface';

@Component({
  selector: 'app-pacientes',
  standalone: true,
  imports: [CommonModule, RouterLink],
  templateUrl: './pacientes.html',
  styleUrls: ['./pacientes.scss']
})
export class PacientesComponent implements OnInit {

  cargando = signal<boolean>(true);
  pacientes = signal<NinoResumenTerapeuta[]>([]);
  filtrados = signal<NinoResumenTerapeuta[]>([]);

  busqueda = signal<string>('');

  constructor(private pacientesService: TerapeutaPacientesService) {}

  ngOnInit(): void {
    this.cargarPacientes();
  }

  cargarPacientes() {
    this.cargando.set(true);

    this.pacientesService.getPacientesAsignados().subscribe({
      next: (lista) => {
        this.pacientes.set(lista);
        this.filtrados.set(lista);
        this.cargando.set(false);
      },
      error: () => {
        this.cargando.set(false);
      }
    });
  }

  filtrar(e: Event) {
    const term = (e.target as HTMLInputElement).value.toLowerCase();
    this.busqueda.set(term);

    const filtered = this.pacientes().filter(p =>
      p.nombreCompleto.toLowerCase().includes(term)
    );

    this.filtrados.set(filtered);
  }
}
