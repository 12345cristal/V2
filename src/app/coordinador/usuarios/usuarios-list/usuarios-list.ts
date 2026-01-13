import { Component, Input, Output, EventEmitter } from '@angular/core';
import { CommonModule } from '@angular/common';
import { MatIconModule } from '@angular/material/icon';

import type { UsuarioListado } from '../../../interfaces/usuario.interface';

@Component({
  selector: 'app-usuarios-list',
  standalone: true,
  imports: [
    CommonModule,
    MatIconModule
  ],
  templateUrl: './usuarios-list.html',
  styleUrls: ['./usuarios-list.scss']
})
export class UsuariosListComponent {

  @Input({ required: true })
  usuarios: UsuarioListado[] = [];

  @Output()
  editar = new EventEmitter<UsuarioListado>();

  @Output()
  cambiarEstado = new EventEmitter<UsuarioListado>();
}
