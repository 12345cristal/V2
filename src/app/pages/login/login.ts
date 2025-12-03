import { Component, signal } from '@angular/core';
import { CommonModule } from '@angular/common';
import {
  FormBuilder,
  FormGroup,
  Validators,
  ReactiveFormsModule
} from '@angular/forms';
import { Router } from '@angular/router';

import { AuthService } from '../../auth/auth.service';
import { HeaderComponent } from '../../shared/header/header';
import { FooterComponent } from '../../shared/footer/footer';

@Component({
  selector: 'app-login',
  standalone: true,
  imports: [
    CommonModule,
    ReactiveFormsModule,
    HeaderComponent,
    FooterComponent
  ],
  templateUrl: './login.html',
  styleUrls: ['./login.scss']
})
export class Login {

  loginForm: FormGroup;

  mostrarPassword = false;

  // ALERTA GLOBAL ESTILIZADA (usa alert-error de tu SCSS)
  mensajeError = signal<string>('');

  constructor(
    private fb: FormBuilder,
    private authService: AuthService,
    private router: Router
  ) {

    // FORMULARIO REACTIVO
    this.loginForm = this.fb.group({
      correo: ['', [Validators.required, Validators.email]],
      contrasena: ['', [Validators.required, Validators.minLength(6)]],
    });
  }

  // ===============================
  // 🔄 MOSTRAR ALERTA + AUTOCIERRE
  // ===============================
  mostrarAlerta(msg: string) {
    this.mensajeError.set(msg);

    setTimeout(() => {
      this.mensajeError.set('');
    }, 3500);
  }

  togglePassword(): void {
    this.mostrarPassword = !this.mostrarPassword;
  }

  // ===============================
  // 🚀 FUNCIÓN LOGIN
  // ===============================
  login(): void {

    // ------ 1) CAMPOS VACÍOS ------
    if (!this.loginForm.get('correo')?.value && !this.loginForm.get('contrasena')?.value) {
      this.mostrarAlerta('Por favor ingresa tus datos.');
      return;
    }

    // ------ 2) FORMULARIO INVALIDO ------
    if (this.loginForm.invalid) {

      if (this.loginForm.get('correo')?.errors?.['email']) {
        this.mostrarAlerta('El correo no es válido.');
      } else if (this.loginForm.get('contrasena')?.errors?.['minlength']) {
        this.mostrarAlerta('La contraseña debe tener mínimo 6 caracteres.');
      } else {
        this.mostrarAlerta('Revisa los campos del formulario.');
      }

      return;
    }

    const { correo, contrasena } = this.loginForm.value;

    // ------ 3) PETICIÓN AL SERVIDOR ------
    this.authService.login(correo, contrasena).subscribe({

      next: (response) => {

        if (!response?.token?.access_token || !response.user) {
          this.mostrarAlerta('Respuesta inesperada del servidor.');
          return;
        }

        // Guardar datos
        localStorage.setItem('token', response.token.access_token);
        localStorage.setItem('user', JSON.stringify(response.user));

        // Redirección según rol
        const rol = response.user.rol_id;

        switch (rol) {
          case 1:
            this.router.navigate(['/administrador/inicio']);
            break;
          case 2:
            this.router.navigate(['/coordinador/inicio']);
            break;
          case 3:
            this.router.navigate(['/terapeuta/inicio']);
            break;
          case 4:
            this.router.navigate(['/padre/inicio']);
            break;

          default:
            this.router.navigate(['/']);
        }

        this.mensajeError.set('');
      },

      error: (err) => {

        console.error('❌ Error al iniciar sesión:', err);

        // ------ 4) MANEJO DE ERRORES DEL BACKEND ------
        if (err.status === 401) {
          this.mostrarAlerta('Correo o contraseña incorrectos.');
          return;
        }

        if (err.status === 0) {
          this.mostrarAlerta('No hay conexión con el servidor.');
          return;
        }

        const message =
          err.error?.detail ||
          err.error?.message ||
          (typeof err.error === 'string' ? err.error : null);

        if (message) {
          this.mostrarAlerta(message);
          return;
        }

        this.mostrarAlerta('Ocurrió un error inesperado.');
      }
    });
  }
}
