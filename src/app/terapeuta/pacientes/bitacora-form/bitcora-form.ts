import { Component, EventEmitter, Input, Output } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormBuilder, ReactiveFormsModule, Validators, FormGroup } from '@angular/forms';

export interface BitacoraFormPayload {
  comportamiento: string;
  avance: string;
  actividadesRealizadas: string;
  recomendaciones: string;
  progresoSesion: number;
}

@Component({
  selector: 'app-bitacora-form',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule],
  templateUrl: './bitacora-form.html',
  styleUrls: ['./bitacora-form.scss']
})
export class BitacoraFormComponent {

  @Input() bloqueado = false;  
  @Output() submitBitacora = new EventEmitter<BitacoraFormPayload>();

  form!: FormGroup; // se declara aquí, se inicializa después

  constructor(private fb: FormBuilder) {
    this.form = this.fb.group({
      comportamiento: ['', [Validators.required, Validators.minLength(10)]],
      avance: ['', [Validators.required, Validators.minLength(10)]],
      actividadesRealizadas: ['', [Validators.required, Validators.minLength(5)]],
      recomendaciones: [''],
      progresoSesion: [0, [Validators.required, Validators.min(0), Validators.max(100)]]
    });
  }

  enviar() {
    if (this.form.invalid || this.bloqueado) {
      this.form.markAllAsTouched();
      return;
    }

    this.submitBitacora.emit(this.form.value as BitacoraFormPayload);

    this.form.reset({ progresoSesion: 0 });
  }
}
