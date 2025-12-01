// src/app/ninos/pages/nino-terapias/nino-terapias.component.ts

import { Component, OnInit, computed, signal } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ActivatedRoute, RouterModule } from '@angular/router';

import {
  NinoResumen,
  NinoTerapiasDetalle,
  TerapiaAsignadaNino,
  TipoTerapiaNino
} from '../../interfaces/terapias-nino.interface';

import { TerapiasNinoService } from '../../service/terapias-nino.service';

@Component({
  selector: 'app-nino-terapias',
  standalone: true,
  imports: [CommonModule, RouterModule],
  templateUrl: './terapias.html',
  styleUrls: ['./terapias.scss']
})
export class TerapiasComponent implements OnInit {

  // Estado principal
  nino = signal<NinoResumen | null>(null);
  terapias = signal<TerapiaAsignadaNino[]>([]);

  // Estado de UI
  cargando = signal<boolean>(false);
  error = signal<string | null>(null);

  // Filtro por tipo de terapia (opcional)
  filtroTipo = signal<TipoTerapiaNino | 'TODAS'>('TODAS');

  // Computed: terapias filtradas
  terapiasFiltradas = computed(() => {
    const tipo = this.filtroTipo();
    const lista = this.terapias();

    if (tipo === 'TODAS') return lista;
    return lista.filter(t => t.tipo_terapia === tipo);
  });

  constructor(
    private route: ActivatedRoute,
    private terapiasNinoService: TerapiasNinoService
  ) {}

  ngOnInit(): void {
    const idNinoParam = this.route.snapshot.paramMap.get('id');
    const idNino = idNinoParam ? Number(idNinoParam) : NaN;

    if (isNaN(idNino)) {
      this.error.set('No se encontró el identificador del niño.');
      return;
    }

    this.cargarTerapiasDeNino(idNino);
  }

  private cargarTerapiasDeNino(idNino: number): void {
    this.cargando.set(true);
    this.error.set(null);

    this.terapiasNinoService.obtenerTerapiasDeNino(idNino).subscribe({
      next: (data: NinoTerapiasDetalle) => {
        this.nino.set(data.nino);
        this.terapias.set(data.terapias ?? []);
        this.cargando.set(false);
      },
      error: (err) => {
        console.error('Error al cargar terapias del niño', err);
        this.error.set('Ocurrió un error al cargar las terapias del niño.');
        this.cargando.set(false);
      }
    });
  }

  seleccionarFiltro(tipo: TipoTerapiaNino | 'TODAS'): void {
    this.filtroTipo.set(tipo);
  }

  // Helpers para la vista
  obtenerIniciales(nombreCompleto: string | undefined | null): string {
    if (!nombreCompleto) return '';
    const partes = nombreCompleto.trim().split(' ');
    const primeras = partes.slice(0, 2);
    return primeras.map(p => p.charAt(0).toUpperCase()).join('');
  }

  formatearFecha(fechaIso?: string | null): string {
    if (!fechaIso) return '—';
    const fecha = new Date(fechaIso);
    if (isNaN(fecha.getTime())) return '—';
    return fecha.toLocaleDateString('es-MX', {
      year: 'numeric',
      month: 'short',
      day: '2-digit'
    });
  }
}
