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
  ninoId!: number;

  tareas: TareaRecurso[] = [];

  /** control de edición por tarea */
  editando: Record<number, boolean> = {};

  /** buffer temporal de notas */
  notasTmp: Record<number, string> = {};

  constructor(
    private route: ActivatedRoute,
    private tareasService: TareasService
  ) {
    const id = this.route.snapshot.paramMap.get('ninoId');
    this.ninoId = id ? Number(id) : 0;

    if (this.ninoId) {
      this.cargar();
    }
  }

  cargar(): void {
    this.tareasService
      .getTareasPorNino(this.ninoId)
      .subscribe((resp: TareaRecurso[]) => {
        this.tareas = resp;

        // inicializar notas temporales
        for (const t of this.tareas) {
          this.notasTmp[t.id] = t.notas_terapeuta ?? '';
          this.editando[t.id] = false;
        }
      });
  }

  toggleCompletado(t: TareaRecurso): void {
    this.tareasService
      .actualizarEstado(t.id, !t.completado)
      .subscribe(() => {
        t.completado = !t.completado;
      });
  }

  activarEdicion(t: TareaRecurso): void {
    this.editando[t.id] = true;
    this.notasTmp[t.id] = t.notas_terapeuta ?? '';
  }

  cancelarEdicion(t: TareaRecurso): void {
    this.editando[t.id] = false;
    this.notasTmp[t.id] = t.notas_terapeuta ?? '';
  }

  guardarNotas(t: TareaRecurso): void {
    const notas = this.notasTmp[t.id];

    this.tareasService
      .actualizarNotasTerapeuta(t.id, notas)
      .subscribe(() => {
        t.notas_terapeuta = notas;
        this.editando[t.id] = false;
      });
  }
}
