// src/app/coordinador/usuarios/usuarios.ts
import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import {
  FormBuilder,
  FormGroup,
  Validators,
  ReactiveFormsModule
} from '@angular/forms';
import { MatIconModule } from '@angular/material/icon';
import { RouterModule } from '@angular/router';

import {
  UsuarioService,
  CrearUsuarioDto,
  ActualizarUsuarioDto
} from '../../service/usuario.service';

import { UsuariosListComponent } from './usuarios-list/usuarios-list';
import { UsuarioFormComponent } from './usuarios-form/usuarios-form';

import type { UsuarioListado, Personal } from '../../interfaces/usuario.interface';
import type { Rol } from '../../interfaces/rol.interface';

@Component({
  selector: 'app-gestion-usuarios',
  standalone: true,
  imports: [
    CommonModule,
    ReactiveFormsModule,
    MatIconModule,
    RouterModule,
    UsuariosListComponent,
    UsuarioFormComponent
  ],
  templateUrl: './usuarios.html',
  styleUrls: ['./usuarios.scss']
})
export class UsuariosComponent implements OnInit {

  // ===========================================================
  // LISTAS
  // ===========================================================
  usuarios: UsuarioListado[] = [];
  usuariosFiltrados: UsuarioListado[] = [];
  personalSinUsuario: Personal[] = [];
  rolesSistema: Rol[] = [];   // 🔥 VIENEN DE BD

  cargandoUsuarios = false;
  cargandoPersonal = false;

  errorGeneral: string | null = null;
  mensajeOk: string | null = null;

  // ===========================================================
  // FORMULARIO
  // ===========================================================
  formUsuario!: FormGroup;
  modoEdicion = false;
  usuarioSeleccionado: UsuarioListado | null = null;
  mostrarErrores = false;

  mostrarFormulario = false;

  constructor(
    private fb: FormBuilder,
    private usuarioService: UsuarioService
  ) {
    this.crearFormulario();
  }

  ngOnInit(): void {
    this.cargarDatos();
    this.cargarRoles();
  }

  // ===========================================================
  // FORMULARIO BASE
  // ===========================================================
  crearFormulario(): void {
    this.formUsuario = this.fb.group(
      {
        id_usuario: [null],
        id_personal: [null, Validators.required],

        username: ['', [
          Validators.required,
          Validators.minLength(4),
          Validators.maxLength(30),
          Validators.pattern(/^[a-zA-Z0-9._-]+$/)
        ]],

        rol_sistema: ['', Validators.required],
        estado: ['ACTIVO', Validators.required],
        debe_cambiar_password: [true],

        password: [''],
        confirmarPassword: [''],
        cambiarPassword: [false]
      },
      { validators: this.passwordsIgualesValidator('password', 'confirmarPassword') }
    );
  }

  // ===========================================================
  // CARGAR USUARIOS Y PERSONAL
  // ===========================================================
  cargarDatos(): void {
    this.cargandoUsuarios = true;

    this.usuarioService.getUsuarios().subscribe({
      next: data => {
        this.usuarios = data;
        this.usuariosFiltrados = [...data];
        this.cargandoUsuarios = false;
      }
    });

    this.usuarioService.getPersonalSinUsuario().subscribe({
      next: data => this.personalSinUsuario = data
    });
  }

  // ===========================================================
  // CARGAR ROLES DESDE BD
  // ===========================================================
  cargarRoles(): void {
    this.usuarioService.getRoles().subscribe({
      next: roles => this.rolesSistema = roles,
      error: () => this.errorGeneral = "Error al cargar los roles."
    });
  }

  // ===========================================================
  // NUEVO USUARIO
  // ===========================================================
  nuevoUsuario() {
    this.modoEdicion = false;
    this.mostrarFormulario = true;
    this.mostrarErrores = false;

    this.formUsuario.reset({
      id_usuario: null,
      id_personal: null,
      username: '',
      rol_sistema: '',
      estado: 'ACTIVO',
      debe_cambiar_password: true,
      password: '',
      confirmarPassword: '',
      cambiarPassword: true
    });
  }

  cerrarFormulario() {
    this.mostrarFormulario = false;
    this.formUsuario.reset();
  }

  // ===========================================================
  // ASIGNAR PERSONAL DESDE LISTA
  // ===========================================================
  asignarDesdePersonal(p: Personal) {
    this.nuevoUsuario();
    this.formUsuario.patchValue({
      id_personal: p.id_personal,
      username: this.generarUsernameSugerido(p),
      rol_sistema: 'TERAPEUTA'
    });
  }

  // ===========================================================
  // EDITAR USUARIO
  // ===========================================================
  editarUsuario(u: UsuarioListado) {
    this.modoEdicion = true;
    this.mostrarFormulario = true;

    this.formUsuario.setValue({
      id_usuario: u.id_usuario,
      id_personal: u.id_personal,
      username: u.username,
      rol_sistema: u.rol_sistema,
      estado: u.estado,
      debe_cambiar_password: u.debe_cambiar_password ?? false,
      password: '',
      confirmarPassword: '',
      cambiarPassword: false
    });
  }

  // ===========================================================
  // CAMBIAR ESTADO
  // ===========================================================
  cambiarEstado(u: UsuarioListado) {
    const nuevoEstado = u.estado === 'ACTIVO' ? 'INACTIVO' : 'ACTIVO';

    this.usuarioService.cambiarEstado(u.id_usuario!, nuevoEstado).subscribe({
      next: resp => u.estado = resp.estado
    });
  }

  // ===========================================================
  // GUARDAR USUARIO
  // ===========================================================
  guardarUsuario() {
    this.mostrarErrores = true;

    if (this.formUsuario.invalid) {
      this.formUsuario.markAllAsTouched();
      return;
    }

    const data = this.formUsuario.value;

    // --------- EDITAR ----------
    if (this.modoEdicion) {
      const payload: ActualizarUsuarioDto = {
        username: data.username,
        rol_sistema: data.rol_sistema,
        estado: data.estado
      };

      this.usuarioService.actualizarUsuario(data.id_usuario, payload).subscribe({
        next: () => {
          this.cargarDatos();
          this.cerrarFormulario();
        }
      });

      return;
    }

    // --------- CREAR ----------
    const payloadNuevo: CrearUsuarioDto = {
      id_personal: data.id_personal,
      username: data.username,
      password: data.password,
      rol_sistema: data.rol_sistema,
      debe_cambiar_password: data.debe_cambiar_password
    };

    this.usuarioService.crearUsuario(payloadNuevo).subscribe({
      next: () => {
        this.cargarDatos();
        this.cerrarFormulario();
      }
    });
  }

  // ===========================================================
  // FILTRO
  // ===========================================================
  aplicarFiltro(texto: string) {
    texto = texto.trim().toLowerCase();
    this.usuariosFiltrados = this.usuarios.filter(u =>
      (u.username + ' ' + u.nombre_completo + ' ' + u.rol_sistema)
        .toLowerCase()
        .includes(texto)
    );
  }

  // ===========================================================
  // AUXILIARES
  // ===========================================================
  generarUsernameSugerido(p: Personal): string {
    return (p.nombres.split(' ')[0] + '.' + p.apellido_paterno)
      .toLowerCase()
      .replace(/[^a-z0-9._-]/g, '');
  }

  passwordsIgualesValidator(pass: string, confirm: string) {
    return (fg: FormGroup) => {
      if (fg.get(pass)?.value !== fg.get(confirm)?.value) {
        fg.get(confirm)?.setErrors({ passwordMismatch: true });
      }
    };
  }
}
