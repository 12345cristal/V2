// src/app/coordinador/usuarios/usuarios.ts
import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormBuilder, FormGroup, ReactiveFormsModule, Validators } from '@angular/forms';
import { MatIconModule } from '@angular/material/icon';
import { RouterModule } from '@angular/router';

import { UsuariosListComponent } from './usuarios-list/usuarios-list';
import { UsuarioFormComponent } from './usuarios-form/usuarios-form';

import { UsuarioService } from '../../service/usuario.service';
import type { UsuarioListado, Personal, Rol, ActualizarUsuarioDto } from '../../interfaces/usuario.interface';
import type { CrearUsuarioDto } from '../../interfaces/usuario.interface';

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
  personalFiltrado: Personal[] = [];  // 🔥 NUEVO: para filtrado
  rolesSistema: Rol[] = [];

  cargandoUsuarios = false;
  cargandoPersonal = false;

  errorGeneral: string | null = null;
  mensajeOk: string | null = null;

  // 🔥 NUEVO: controlar vista
  vistaActual: 'usuarios' | 'personal' = 'usuarios';

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

        email: ['', [Validators.required, Validators.email]],
        rol_id: [null, Validators.required],
        estado: ['ACTIVO', Validators.required],

        password: ['', [Validators.minLength(8)]],
        confirmarPassword: ['', [Validators.minLength(8)]],
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
    this.cargandoPersonal = true;
    this.errorGeneral = null;

    this.usuarioService.getUsuarios().subscribe({
      next: (data: UsuarioListado[]) => {
        this.usuarios = data;
        this.usuariosFiltrados = [...data];
        this.cargandoUsuarios = false;
      },
      error: (err: any) => {
        console.error('Error al cargar usuarios:', err);
        this.errorGeneral = 'No se pudieron cargar los usuarios. Verifica la conexión con el servidor.';
        this.cargandoUsuarios = false;
      }
    });

    this.usuarioService.getPersonalSinUsuario().subscribe({
      next: (data: Personal[]) => {
        this.personalSinUsuario = data;
        this.personalFiltrado = [...data];  // 🔥 NUEVO
        this.cargandoPersonal = false;
      },
      error: (err: any) => {
        console.error('Error al cargar personal sin usuario:', err);
        this.errorGeneral = 'No se pudo cargar el personal disponible.';
        this.cargandoPersonal = false;
      }
    });
  }

  // ===========================================================
  // CARGAR ROLES DESDE BD
  // ===========================================================
  cargarRoles(): void {
    this.usuarioService.getRoles().subscribe({
      next: (roles: Rol[]) => this.rolesSistema = roles,
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
      email: '',
      rol_id: null,
      estado: 'ACTIVO',
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
      email: p.correo_personal,
      rol_id: p.id_rol
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
      id_personal: u.id_personal ?? null,
      email: u.email,
      rol_id: u.rol_id,
      estado: u.estado,
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
      next: (resp: any) => u.estado = resp.estado
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
        email: data.email,
        rol_id: data.rol_id,
        estado: data.estado
      };

      if (data.cambiarPassword && data.password) {
        payload.password = data.password;
      }

      this.usuarioService.actualizarUsuario(data.id_usuario, payload).subscribe({
        next: () => {
          this.cargarDatos();
          this.cerrarFormulario();
        }
      });

      return;
    }

    // --------- CREAR ----------
    const personal = this.personalSinUsuario.find(p => p.id_personal === data.id_personal);
    if (!personal) {
      this.errorGeneral = 'Debes seleccionar un personal válido';
      return;
    }

    const payloadNuevo: CrearUsuarioDto = {
      id_personal: personal.id_personal!,
      nombres: personal.nombres,
      apellido_paterno: personal.apellido_paterno,
      email: data.email,
      password: data.password,
      rol_id: data.rol_id,
    };

   this.usuarioService.crearUsuario(payloadNuevo).subscribe({
      next: () => {
        this.cargarDatos();
        this.cerrarFormulario();
      }
    });
  }

  // ===========================================================
  // 🔥 NUEVO: CAMBIAR VISTA
  // ===========================================================
  cambiarVista(vista: 'usuarios' | 'personal') {
    this.vistaActual = vista;
    this.cerrarFormulario();
  }

  // ===========================================================
  // FILTRO
  // ===========================================================
  aplicarFiltro(texto: string) {
    texto = texto.trim().toLowerCase();
    
    if (this.vistaActual === 'usuarios') {
      this.usuariosFiltrados = this.usuarios.filter(u =>
        (u.email + ' ' + u.nombre_completo + ' ' + u.nombre_rol)
          .toLowerCase()
          .includes(texto)
      );
    } else {
      // 🔥 NUEVO: filtrar personal
      this.personalFiltrado = this.personalSinUsuario.filter(p =>
        (p.nombres + ' ' + p.apellido_paterno + ' ' + (p.apellido_materno || '') + ' ' + (p.correo_personal || ''))
          .toLowerCase()
          .includes(texto)
      );
    }
  }

  // ===========================================================
  // AUXILIARES
  // ===========================================================
  passwordsIgualesValidator(pass: string, confirm: string) {
    return (fg: FormGroup) => {
      if (fg.get(pass)?.value !== fg.get(confirm)?.value) {
        fg.get(confirm)?.setErrors({ passwordMismatch: true });
      }
    };
  }
}
