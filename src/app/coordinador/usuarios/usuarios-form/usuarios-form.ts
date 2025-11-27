import { Component, Input, Output, EventEmitter } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ReactiveFormsModule, FormGroup } from '@angular/forms';
import { MatIconModule } from '@angular/material/icon';
import type { Personal } from '../../interfaces/usuario.interface';

@Component({
  selector: 'app-usuario-form',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule, MatIconModule],
  templateUrl: './usuarios-form.html',
  styleUrls: ['./usuarios-form.scss']
})
export class UsuarioFormComponent {

  @Input() form!: FormGroup;
  @Input() personalSinUsuario: Personal[] = [];
  @Input() modoEdicion = false;
  @Input() mostrarErrores = false;

  @Output() guardar = new EventEmitter<void>();
  @Output() limpiar = new EventEmitter<void>();

  get f() { return this.form.controls; }

  get passwordControl() { return this.form.get('password'); }
  get confirmarPasswordControl() { return this.form.get('confirmarPassword'); }

  get reglasPassword() {
    const pass = this.passwordControl?.value || '';
    return {
      length: pass.length >= 8,
      mayus: /[A-Z]/.test(pass),
      minus: /[a-z]/.test(pass),
      numero: /\d/.test(pass),
      simbolo: /[^A-Za-z0-9]/.test(pass)
    };
  }
}
