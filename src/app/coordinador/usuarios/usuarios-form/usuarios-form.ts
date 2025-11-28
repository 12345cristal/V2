import { Component, Input, Output, EventEmitter } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ReactiveFormsModule, FormGroup } from '@angular/forms';
import { MatIconModule } from '@angular/material/icon';

import type { Personal } from '../../../interfaces/usuario.interface';
import type { Rol } from '../../../interfaces/rol.interface';

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
  @Input() rolesSistema: Rol[] = [];
  @Input() estadosSistema: string[] = [];
  @Input() modoEdicion = false;
  @Input() mostrarErrores = false;

  @Output() guardar = new EventEmitter<void>();
  @Output() salir = new EventEmitter<void>();

  // GETTERS
  get f() { return this.form.controls; }
  get passwordControl() { return this.form.get('password'); }
  get confirmarPasswordControl() { return this.form.get('confirmarPassword'); }

  get reglasPassword() {
    const p = this.passwordControl?.value || '';
    return {
      length: p.length >= 8,
      mayus: /[A-Z]/.test(p),
      minus: /[a-z]/.test(p),
      numero: /\d/.test(p),
      simbolo: /[^A-Za-z0-9]/.test(p),
    };
  }

  // ================================
  // 🔵 LIMPIAR SIN CERRAR FORMULARIO
  // ================================
  limpiarFormulario() {
    // SOLO limpiamos lo editable
    this.form.patchValue({
      id_personal: null,
      username: '',
      rol_sistema: '',
      estado: this.estadosSistema[0] ?? 'ACTIVO',

      // Contraseñas siempre limpias
      password: '',
      confirmarPassword: '',

      // Checkbox depende si está editando
      cambiarPassword: !this.modoEdicion,
      debe_cambiar_password: true,
    });

    // Limpiamos validaciones visuales
    this.form.markAsUntouched();
    this.form.markAsPristine();
  }

  // ================================
  // 🔵 GUARDAR
  // ================================
  guardarUsuario() {
    this.mostrarErrores = true;

    if (this.form.invalid) {
      this.form.markAllAsTouched();
      return;
    }

    if (!this.modoEdicion) {
      if (!this.passwordControl?.value || !this.confirmarPasswordControl?.value) {
        return;
      }
    }

    if (this.modoEdicion && this.f['cambiarPassword']?.value) {
      if (!this.passwordControl?.value || !this.confirmarPasswordControl?.value) {
        return;
      }
    }

    this.guardar.emit();
  }

  // ================================
  // 🔵 SALIR
  // ================================
  salirAlListado() {
    this.salir.emit();
  }
}
