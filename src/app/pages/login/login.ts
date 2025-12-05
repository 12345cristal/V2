import { Component, signal } from '@angular/core';
import { CommonModule } from '@angular/common';
import {
  FormBuilder,
  FormGroup,
  Validators,
  ReactiveFormsModule,
  AbstractControl
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
export class LoginComponent {

  // =============================
  // FORMULARIO
  // =============================
  loginForm!: FormGroup;  // se crea en constructor

  // =============================
  // ESTADO
  // =============================
  mostrarPassword = false;
  mensajeError = signal<string>('');

  constructor(
    private fb: FormBuilder,
    private authService: AuthService,
    private router: Router
  ) {
    this.loginForm = this.fb.group({
      correo: ['', [Validators.required, Validators.email]],
      contrasena: ['', [Validators.required, Validators.minLength(6)]],
    });
  }

  // =============================
  // MÉTODO ACCESIBLE EN EL HTML
  // =============================
  public control(name: string): AbstractControl {
    return this.loginForm.get(name)!;
  }

  mostrarAlerta(msg: string): void {
    this.mensajeError.set(msg);
    setTimeout(() => this.mensajeError.set(''), 3500);
  }

  togglePassword(): void {
    this.mostrarPassword = !this.mostrarPassword;
  }

  // =============================
  // 🚀 LOGIN
  // =============================
  login(): void {
    if (this.loginForm.invalid) {
      this.loginForm.markAllAsTouched();
      this.mostrarAlerta('Completa correctamente el formulario.');
      return;
    }

    const { correo, contrasena } = this.loginForm.value;

    this.authService.login(correo, contrasena).subscribe({
      next: (response) => {

        if (!response?.token?.access_token || !response.user) {
          this.mostrarAlerta('Error inesperado del servidor.');
          return;
        }

        localStorage.setItem('token', response.token.access_token);
        localStorage.setItem('user', JSON.stringify(response.user));

        const rol = response.user.rol_id;

        const rutas: Record<number, string> = {
          1: '/administrador/inicio',
          2: '/coordinador/inicio',
          3: '/terapeuta/inicio',
          4: '/padre/inicio',
        };

        this.router.navigate([rutas[rol] || '/']);
      },

      error: (err) => {
        if (err.status === 401) return this.mostrarAlerta('Correo o contraseña incorrectos.');
        if (err.status === 403) return this.mostrarAlerta('Tu cuenta está inactiva.');
        if (err.status === 0)   return this.mostrarAlerta('No hay conexión con el servidor.');

        const msg =
          err.error?.detail ||
          err.error?.message ||
          (typeof err.error === 'string' ? err.error : 'Ocurrió un error inesperado.');

        this.mostrarAlerta(msg);
      }
    });
  }
}
