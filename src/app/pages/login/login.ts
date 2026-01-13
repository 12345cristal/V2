import { Component, signal, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import {
  NonNullableFormBuilder,
  FormGroup,
  Validators,
  ReactiveFormsModule,
  AbstractControl
} from '@angular/forms';
import { Router } from '@angular/router';

import { AuthService } from '../../auth/auth.service';
import { HeaderComponent } from '../../shared/header/header';
import { FooterComponent } from '../../shared/footer/footer';
import { HealthCheckService } from '../../service/health-check.service';

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

  loginForm: FormGroup;
  mostrarPassword = false;
  mensajeError = signal<string>('');
  backendUp = signal<boolean>(true);

  private fb = inject(NonNullableFormBuilder);
  private authService = inject(AuthService);
  private router = inject(Router);
  private health = inject(HealthCheckService);

  constructor() {
    this.loginForm = this.fb.group({
      correo: ['', [Validators.required, Validators.email]],
      contrasena: ['', [Validators.required, Validators.minLength(6)]],
    });

    // 🔍 Check real del backend
    this.health.checkApi().subscribe(status => {
      this.backendUp.set(status === 'up');
    });
  }

  control(name: string): AbstractControl {
    return this.loginForm.get(name)!;
  }

  mostrarAlerta(msg: string): void {
    this.mensajeError.set(msg);
    setTimeout(() => this.mensajeError.set(''), 3500);
  }

  togglePassword(): void {
    this.mostrarPassword = !this.mostrarPassword;
  }

  login(): void {
    if (!this.backendUp()) {
      this.mostrarAlerta('El servidor no está disponible.');
      return;
    }

    if (this.loginForm.invalid) {
      this.loginForm.markAllAsTouched();
      this.mostrarAlerta('Completa correctamente el formulario.');
      return;
    }

    const { correo, contrasena } = this.loginForm.getRawValue();

    this.authService.login(correo, contrasena).subscribe({
      next: (response) => {
        const rol = response.user.rol_id;

        const rutas: Record<number, string> = {
          1: '/administrador/inicio',
          2: '/coordinador/inicio',
          3: '/terapeuta/inicio',
          4: '/padre/inicio',
        };

        this.router.navigate([rutas[rol] ?? '/']);
      },
      error: (err) => {
        if (err.status === 401) return this.mostrarAlerta('Correo o contraseña incorrectos.');
        if (err.status === 403) return this.mostrarAlerta('Cuenta inactiva.');
        if (err.status === 0) return this.mostrarAlerta('No hay conexión con el servidor.');
        this.mostrarAlerta('Error inesperado.');
      }
    });
  }
}
