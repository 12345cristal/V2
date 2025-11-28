import { Component, Input, Output, EventEmitter } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ReactiveFormsModule, FormBuilder, Validators } from '@angular/forms';

@Component({
  selector: 'app-bitacora-form',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule],
  templateUrl: './bitacora-form.html',
  styleUrls: ['./bitacora-form.scss']
})
export class BitacoraFormComponent {

  @Input() pacienteId!: number;
  @Output() guardado = new EventEmitter<void>();

  form = this.fb.group({
    comportamiento: ['', Validators.required],
    avance: ['', Validators.required],
    actividadesRealizadas: ['', Validators.required],
    recomendaciones: [''],
    progresoSesion: [0, [Validators.required, Validators.min(0), Validators.max(100)]]
  });

  cargando = false;
  mensajeExito: string | null = null;
  mensajeError: string | null = null;

  constructor(private fb: FormBuilder) {}

  submit() {
    if (this.form.invalid) {
      this.form.markAllAsTouched();
      this.mensajeError = 'Completa todos los campos obligatorios.';
      return;
    }

    const formData = new FormData();
    for (const [key, value] of Object.entries(this.form.value)) {
      formData.append(key, value as string);
    }

    this.guardado.emit(formData);
    this.mensajeExito = 'Bitácora registrada correctamente.';
  }
}
