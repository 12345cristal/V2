import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ActivatedRoute } from '@angular/router';
import { FormsModule } from '@angular/forms';

import { TareasService } from '../../service/terapeuta/tareas.service';
import { TareaRecurso } from '../../interfaces/terapeuta/tarea-recurso.interface';

@Component({
  standalone: true,
  selector: 'app-tareas-nino',
  imports: [CommonModule, FormsModule],
  templateUrl: './tareas-nino.html',
  styleUrls: ['./tareas-nino.scss'],
})
export class TareasNino {
  ninoId = 0;

  tareas: TareaRecurso[] = [];

  /** Control de edición por tarea */
  editando: Record<number, boolean> = {};

  /** Buffer temporal de notas */
  notasTmp: Record<number, string> = {};

  constructor(
    private route: ActivatedRoute,
    private tareasService: TareasService
  ) {
    const id = this.route.snapshot.paramMap.get('ninoId');
    this.ninoId = id ? Number(id) : 0;

    if (this.ninoId > 0) {
      this.cargar();
    }
  }

  // =====================================================
  // CARGAR TAREAS
  // =====================================================
  cargar(): void {
    this.tareasService.getTareasPorNino(this.ninoId).subscribe({
      next: (tareas: TareaRecurso[]) => {
        this.tareas = tareas;

        // Inicializar estados locales
        for (const t of tareas) {
          this.editando[t.id] = false;
          this.notasTmp[t.id] = t.notas_terapeuta ?? '';
        }
      },
      error: (err) => {
        console.error('Error al cargar tareas:', err);
      },
    });
  }

  // =====================================================
  // TOGGLE COMPLETADO
  // =====================================================
  toggleCompletado(t: TareaRecurso): void {
    const nuevoEstado = !t.completado;

    this.tareasService.actualizarEstado(t.id, nuevoEstado).subscribe({
      next: () => {
        t.completado = nuevoEstado;
      },
      error: (err) => {
        console.error('Error al actualizar estado:', err);
      },
    });
  }

  // =====================================================
  // EDICIÓN DE NOTAS
  // =====================================================
  activarEdicion(t: TareaRecurso): void {
    this.editando[t.id] = true;
    this.notasTmp[t.id] = t.notas_terapeuta ?? '';
  }

  cancelarEdicion(t: TareaRecurso): void {
    this.editando[t.id] = false;
    this.notasTmp[t.id] = t.notas_terapeuta ?? '';
  }

  guardarNotas(t: TareaRecurso): void {
    const notas = this.notasTmp[t.id]?.trim() || '';

    this.tareasService.actualizarNotasTerapeuta(t.id, notas).subscribe({
      next: () => {
        t.notas_terapeuta = notas;
        this.editando[t.id] = false;
      },
      error: (err) => {
        console.error('Error al guardar notas:', err);
      },
    });
  }
}
