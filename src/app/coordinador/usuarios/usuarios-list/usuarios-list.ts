import { Component, Input, Output, EventEmitter } from '@angular/core';
import { CommonModule } from '@angular/common';
import { MatIconModule } from '@angular/material/icon';
import { FormsModule } from '@angular/forms'; // 🟦 NECESARIO PARA ngModel
import type { UsuarioListado, Personal } from '../../../interfaces/usuario.interface';

@Component({
  selector: 'app-usuarios-list',
  standalone: true,
  imports: [
    CommonModule,
    MatIconModule,
    FormsModule   // 🟦 IMPORTANTE
  ],
  templateUrl: './usuarios-list.html',
  styleUrls: ['./usuarios-list.scss']
})
export class UsuariosListComponent {

  @Input() cargandoUsuarios = false;
  @Input() cargandoPersonal = false;

  @Input() personalSinUsuario: Personal[] = [];
  @Input() usuariosFiltrados: UsuarioListado[] = [];

  @Output() asignarPersonal = new EventEmitter<Personal>();
  @Output() editar = new EventEmitter<UsuarioListado>();
  @Output() cambiarEstado = new EventEmitter<UsuarioListado>();
  @Output() filtrar = new EventEmitter<string>();

  filtro = '';

  onFiltroInput() {
    this.filtrar.emit(this.filtro);
  }

  emitirAsignar(p: Personal) {
    this.asignarPersonal.emit(p);
  }

  emitirEditar(u: UsuarioListado) {
    this.editar.emit(u);
  }

  emitirEstado(u: UsuarioListado) {
    this.cambiarEstado.emit(u);
  }
}



