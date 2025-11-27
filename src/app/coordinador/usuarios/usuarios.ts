// src/app/coordinador/pages/gestion-usuarios/gestion-usuarios.ts

import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import {
  FormBuilder,
  FormGroup,
  Validators,
  ReactiveFormsModule,
  AbstractControl
} from '@angular/forms';
import { MatIconModule } from '@angular/material/icon';

import {
  UsuarioService,
  CrearUsuarioDto,
  CambiarPasswordDto,
  ActualizarUsuarioDto
} from '../../service/usuario.service';

import { UsuariosListComponent } from './usuarios-list/usuarios-list';
import { UsuarioFormComponent } from './usuario-form/usuario-form';

import type { UsuarioListado, Personal } from '../interfaces/usuario.interface';

@Component({
  selector: 'app-gestion-usuarios',
  standalone: true,
  imports: [
    CommonModule,
    ReactiveFormsModule,
    MatIconModule,
    UsuariosListComponent,
    UsuarioFormComponent
  ],
  templateUrl: './gestion-usuarios.html',
  styleUrls: ['./gestion-usuarios.scss']
})
export class GestionUsuarios implements OnInit {

  // ===============================
  // LISTADOS
  // ===============================
  usuarios: UsuarioListado[] = [];
  usuariosFiltrados: UsuarioListado[] = [];
  personalSinUsuario: Personal[] = [];

  // ===============================
  // ESTADOS DE UI
  // ===============================
  cargando = false;
  cargandoUsuarios = false;
  cargandoPersonal = false;

  errorGeneral: string | null = null;
  mensajeOk: string | null = null;

  // ===============================
  // FORMULARIO
  // ===============================
  formUsuario!: FormGroup;
  modoEdicion = false;        // false = crear, true = editar
  usuarioSeleccionado: UsuarioListado | null = null;
  mostrarErrores = false;

  // Filtro para la tabla
  filtroTexto = '';

  constructor(
    private fb: FormBuilder,
    private usuarioService: UsuarioService
  ) {
    this.crearFormulario();
  }

  ngOnInit(): void {
    this.cargarDatos();
  }

  // =======================================
  // FORMULARIO REACTIVO
  // =======================================
  crearFormulario(): void {
    this.formUsuario = this.fb.group(
      {
        id_usuario: [null],
        id_personal: [null, Validators.required],
        username: [
          '',
          [
            Validators.required,
            Validators.minLength(4),
            Validators.maxLength(30),
            Validators.pattern(/^[a-zA-Z0-9._-]+$/)
          ]
        ],
        rol_sistema: ['', Validators.required],
        estado: ['ACTIVO', Validators.required],
        debe_cambiar_password: [true],
        password: [''],
        confirmarPassword: [''],
        cambiarPassword: [false]
      },
      { validators: this.passwordsIgualesValidator('password', 'confirmarPassword') }
    );

    // Cuando el checkbox "cambiar contraseña" cambia
    this.formUsuario.get('cambiarPassword')?.valueChanges.subscribe((value: boolean) => {
      this.configurarValidadoresPassword(value);
    });
  }

  get f(): { [key: string]: AbstractControl } {
    return this.formUsuario.controls;
  }

  get passwordControl(): AbstractControl | null {
    return this.formUsuario.get('password');
  }

  get confirmarPasswordControl(): AbstractControl | null {
    return this.formUsuario.get('confirmarPassword');
  }

  // ===================================================
  // VALIDADORES
  // ===================================================
  passwordsIgualesValidator(passField: string, confirmField: string) {
    return (formGroup: FormGroup) => {
      const pass = formGroup.get(passField)?.value;
      const confirm = formGroup.get(confirmField)?.value;

      if (pass && confirm && pass !== confirm) {
        formGroup.get(confirmField)?.setErrors({ passwordMismatch: true });
      } else {
        const errors = formGroup.get(confirmField)?.errors;
        if (errors) {
          delete errors['passwordMismatch'];
          if (!Object.keys(errors).length) {
            formGroup.get(confirmField)?.setErrors(null);
          }
        }
      }
    };
  }

  configurarValidadoresPassword(activo: boolean): void {
    const password = this.passwordControl;
    const confirmar = this.confirmarPasswordControl;

    if (!password || !confirmar) return;

    if (!this.modoEdicion || activo) {
      password.setValidators([
        Validators.required,
        Validators.minLength(8),
        Validators.pattern(/^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[^A-Za-z0-9]).{8,}$/)
      ]);
      confirmar.setValidators([Validators.required]);
    } else {
      password.clearValidators();
      confirmar.clearValidators();
      password.setValue('');
      confirmar.setValue('');
    }

    password.updateValueAndValidity();
    confirmar.updateValueAndValidity();
  }

  // ===================================================
  // CARGA DE DATOS
  // ===================================================
  cargarDatos(): void {
    this.cargando = true;
    this.cargandoUsuarios = true;
    this.cargandoPersonal = true;
    this.errorGeneral = null;

    // Usuarios
    this.usuarioService.getUsuarios().subscribe({
      next: (data) => {
        this.usuarios = data;
        this.usuariosFiltrados = [...data];
        this.cargandoUsuarios = false;
        this.cargando = this.cargandoPersonal;
      },
      error: () => {
        this.errorGeneral = 'Error al cargar usuarios.';
        this.cargandoUsuarios = false;
        this.cargando = this.cargandoPersonal;
      }
    });

    // Personal sin usuario
    this.usuarioService.getPersonalSinUsuario().subscribe({
      next: (data) => {
        this.personalSinUsuario = data;
        this.cargandoPersonal = false;
        this.cargando = this.cargandoUsuarios;
      },
      error: () => {
        this.errorGeneral = 'Error al cargar el personal sin usuario.';
        this.cargandoPersonal = false;
        this.cargando = this.cargandoUsuarios;
      }
    });
  }

  // ===================================================
  // EVENTOS - LISTA
  // ===================================================
  asignarDesdePersonal(personal: Personal): void {
    this.nuevoUsuario();
    this.formUsuario.patchValue({
      id_personal: personal.id_personal,
      username: this.generarUsernameSugerido(personal),
      rol_sistema: 'TERAPEUTA'
    });
  }

  editarUsuario(usuario: UsuarioListado): void {
    this.modoEdicion = true;
    this.usuarioSeleccionado = usuario;
    this.mostrarErrores = false;

    this.formUsuario.reset({
      id_usuario: usuario.id_usuario,
      id_personal: usuario.id_personal,
      username: usuario.username,
      rol_sistema: usuario.rol_sistema,
      estado: usuario.estado,
      debe_cambiar_password: usuario.debe_cambiar_password ?? false,
      password: '',
      confirmarPassword: '',
      cambiarPassword: false
    });

    this.configurarValidadoresPassword(false);
  }

  cambiarEstado(usuario: UsuarioListado): void {
    const nuevoEstado = usuario.estado === 'ACTIVO' ? 'INACTIVO' : 'ACTIVO';

    this.usuarioService.cambiarEstado(usuario.id_usuario!, nuevoEstado).subscribe({
      next: (resp) => {
        usuario.estado = resp.estado;
        this.mensajeOk = `Usuario ${resp.username} ahora está ${resp.estado}.`;
        setTimeout(() => (this.mensajeOk = null), 3500);
      },
      error: () => {
        this.errorGeneral = 'No se pudo cambiar el estado.';
      }
    });
  }

  aplicarFiltro(texto: string): void {
    this.filtroTexto = texto.toLowerCase().trim();

    if (!this.filtroTexto) {
      this.usuariosFiltrados = [...this.usuarios];
      return;
    }

    this.usuariosFiltrados = this.usuarios.filter((u) =>
      (
        u.username +
        ' ' +
        u.nombre_completo +
        ' ' +
        (u.rol_sistema || '')
      )
        .toLowerCase()
        .includes(this.filtroTexto)
    );
  }

  // ===================================================
  // FORM - NUEVO
  // ===================================================
  nuevoUsuario(): void {
    this.modoEdicion = false;
    this.usuarioSeleccionado = null;
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

    this.configurarValidadoresPassword(true);
  }

  // ===================================================
  // GUARDAR
  // ===================================================
  guardarUsuario(): void {
    this.resetMensajes();
    this.mostrarErrores = true;

    if (this.formUsuario.invalid) {
      this.formUsuario.markAllAsTouched();
      this.errorGeneral = 'Hay campos obligatorios sin llenar o con errores.';
      return;
    }

    const data = this.formUsuario.value;

    // =======================
    // ACTUALIZAR
    // =======================
    if (this.modoEdicion && this.usuarioSeleccionado?.id_usuario) {
      const payload: ActualizarUsuarioDto = {
        username: data.username,
        rol_sistema: data.rol_sistema,
        estado: data.estado
      };

      this.usuarioService.actualizarUsuario(this.usuarioSeleccionado.id_usuario, payload)
        .subscribe({
          next: (resp) => {
            this.mensajeOk = `Usuario ${resp.username} actualizado correctamente.`;

            const idx = this.usuarios.findIndex(
              (u) => u.id_usuario === resp.id_usuario
            );

            if (idx >= 0) {
              this.usuarios[idx] = { ...this.usuarios[idx], ...resp };
              this.aplicarFiltro(this.filtroTexto);
            }

            // Cambio de contraseña si aplica
            if (data.cambiarPassword && data.password) {
              const passPayload: CambiarPasswordDto = {
                debe_cambiar_password: data.debe_cambiar_password,
                password: data.password
              };

              this.usuarioService.cambiarPassword(resp.id_usuario!, passPayload)
                .subscribe({
                  next: () => {
                    this.mensajeOk += ' Contraseña actualizada.';
                  }
                });
            }
          },
          error: () => {
            this.errorGeneral = 'No se pudo actualizar el usuario.';
          }
        });

      return;
    }

    // =======================
    // CREAR
    // =======================
    const payloadNuevo: CrearUsuarioDto = {
      id_personal: data.id_personal,
      username: data.username,
      password: data.password,
      rol_sistema: data.rol_sistema,
      debe_cambiar_password: data.debe_cambiar_password
    };

    this.usuarioService.crearUsuario(payloadNuevo).subscribe({
      next: (resp) => {
        this.mensajeOk = `Usuario ${resp.username} creado correctamente.`;
        this.nuevoUsuario();
        this.cargarDatos();
      },
      error: () => {
        this.errorGeneral = 'No se pudo crear el usuario (username repetido).';
      }
    });
  }

  // ============================================
  // AUXILIARES
  // ============================================
  resetMensajes(): void {
    this.errorGeneral = null;
    this.mensajeOk = null;
  }

  generarUsernameSugerido(personal: Personal): string {
    const base =
      (personal.nombres?.split(' ')[0] || '').toLowerCase() +
      '.' +
      (personal.apellido_paterno || '').toLowerCase();

    return base.replace(/[^a-z0-9._-]/gi, '');
  }

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
