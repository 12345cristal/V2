import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import {
  FormBuilder,
  FormGroup,
  Validators,
  ReactiveFormsModule
} from '@angular/forms';
import { Router } from '@angular/router';

import { AuthService } from '../../auth/auth.service';

// Opcionales si tu login tiene header/footer
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
  mensajeError = '';

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

  togglePassword(): void {
    this.mostrarPassword = !this.mostrarPassword;
  }

  login(): void {
    if (this.loginForm.invalid) return;

    const { correo, contrasena } = this.loginForm.value;

    this.authService.login(correo, contrasena).subscribe({
      next: (response) => {
        console.log('✅ Login exitoso:', response);

        // ===============================
        // 🧩 GUARDAR TOKEN + USUARIO
        // ===============================
        localStorage.setItem('token', response.token.access_token);
        localStorage.setItem('user', JSON.stringify(response.user));

        // ===============================
        // 🚀 REDIRIGIR SEGÚN ROL
        // ===============================
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

        this.mensajeError = '';
      },

      error: (err) => {
        console.error('❌ Error al iniciar sesión:', err);
        this.mensajeError =
          err.error?.detail ||
          err.error?.message ||
          (typeof err.error === 'string'
            ? err.error
            : 'Credenciales incorrectas o el servidor no responde.');
      },
    });
  }
}
