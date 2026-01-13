import { Component, Input, Output, EventEmitter } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormGroup, ReactiveFormsModule } from '@angular/forms';
import { MatIconModule } from '@angular/material/icon';
import type { Personal, Rol } from '../../../interfaces/usuario.interface';

@Component({
  selector: 'app-usuario-form',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule, MatIconModule],
  templateUrl: './usuarios-form.html',
  styleUrls: ['./usuarios-form.scss']
})
export class UsuarioFormComponent {
  @Input() formUsuario!: FormGroup;
  @Input() modoEdicion = false;
  @Input() personalSinUsuario: Personal[] = [];
  @Input() rolesSistema: Rol[] = [];
  @Input() mostrarErrores = false;
  
  @Output() guardar = new EventEmitter<void>();
  @Output() cancelar = new EventEmitter<void>();

  onGuardar(): void {
    this.guardar.emit();
  }

  onCancelar(): void {
    this.cancelar.emit();
  }

  get cambiarPassword(): boolean {
    return this.formUsuario.get('cambiarPassword')?.value || false;
  }
}
