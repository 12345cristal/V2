import { Component, EventEmitter, Input, OnChanges, Output, SimpleChanges } from '@angular/core';
import { CommonModule } from '@angular/common';
import {
  ReactiveFormsModule,
  FormBuilder,
  FormGroup
} from '@angular/forms';

import { ActividadesPadreService } from '../../../service/actividades-padre.service';
import {
  ActividadAsignadaPadre,
  CompletarActividadPadreDto,
  CrearValoracionPadreDto
} from '../../../interfaces/actividades-padre.interface';

@Component({
  selector: 'app-padre-actividad-detalle',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule],
  templateUrl: './actividad-detalle.html',
  styleUrls: ['./actividad-detalle.scss']
})
export class ActividadDetalleComponent implements OnChanges {

  @Input() asignacion: ActividadAsignadaPadre | null = null;
  @Output() actualizado = new EventEmitter<void>();

  formCompletar!: FormGroup;
  formRating!: FormGroup;

  guardando = false;

  constructor(
    private fb: FormBuilder,
    private actividadesPadreService: ActividadesPadreService
  ) {
    this.initForms();
  }

  ngOnChanges(changes: SimpleChanges): void {
    if (changes['asignacion'] && this.asignacion) {
      this.resetFormsSegunAsignacion();
    }
  }

  initForms() {
    this.formCompletar = this.fb.group({
      comentariosPadres: ['']
    });

    this.formRating = this.fb.group({
      puntuacion: [0],
      comentario: ['']
    });
  }

  resetFormsSegunAsignacion() {
    if (!this.asignacion) return;

    this.formCompletar.reset({
      comentariosPadres: this.asignacion.comentariosPadres || ''
    });

    this.formRating.reset({
      puntuacion: this.asignacion.ratingTutor || 0,
      comentario: ''
    });
  }

  marcarCompletada() {
    if (!this.asignacion || this.asignacion.completado) return;

    this.guardando = true;

    const dto: CompletarActividadPadreDto = {
      completado: true,
      comentariosPadres: this.formCompletar.value.comentariosPadres || null
    };

    this.actividadesPadreService.completarActividad(this.asignacion.id, dto)
      .subscribe({
        next: () => {
          this.guardando = false;
          this.actualizado.emit();
        },
        error: () => {
          this.guardando = false;
        }
      });
  }

  setRating(value: number) {
    this.formRating.patchValue({ puntuacion: value });
  }

  enviarRating() {
    if (!this.asignacion) return;
    const value = this.formRating.value;

    if (!value.puntuacion || value.puntuacion < 1) {
      return;
    }

    const dto: CrearValoracionPadreDto = {
      puntuacion: value.puntuacion,
      comentario: value.comentario || null
    };

    this.actividadesPadreService.valorarActividad(this.asignacion.id, dto)
      .subscribe({
        next: () => {
          this.actualizado.emit();
        }
      });
  }
}
