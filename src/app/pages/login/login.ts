// src/app/pages/login/login.ts
import { Component, signal, inject, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import {
  NonNullableFormBuilder,
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
export class LoginComponent implements OnInit {

  private fb = inject(NonNullableFormBuilder);
  private auth = inject(AuthService);
  private router = inject(Router);
  private health = inject(HealthCheckService);

  readonly mensajeError = signal('');
  readonly backendStatus = this.health.status;

  mostrarPassword = false;

  readonly loginForm = this.fb.group({
    correo: ['', [Validators.required, Validators.email]],
    contrasena: ['', [Validators.required, Validators.minLength(6)]]
  });

  ngOnInit(): void {
    this.health.check().subscribe();
  }

  control(name: string): AbstractControl {
    return this.loginForm.get(name)!;
  }

  togglePassword(): void {
    this.mostrarPassword = !this.mostrarPassword;
  }

  reintentarBackend(): void {
    this.health.check().subscribe();
  }

  login(): void {
    if (this.backendStatus() === 'down') {
      this.error('El servidor no está disponible');
      return;
    }

    if (this.loginForm.invalid) {
      this.loginForm.markAllAsTouched();
      this.error('Formulario inválido');
      return;
    }

    const { correo, contrasena } = this.loginForm.getRawValue();

    this.auth.login(correo, contrasena).subscribe({
      next: res => {
        const rutas: Record<number, string> = {
          1: '/administrador/inicio',
          2: '/coordinador/inicio',
          3: '/terapeuta/inicio',
          4: '/padre/inicio'
        };
        this.router.navigate([rutas[res.user.rol_id] ?? '/']);
      },
      error: err => {
        if (err.status === 401) this.error('Credenciales incorrectas');
        else if (err.status === 403) this.error('Cuenta inactiva');
        else this.error('Error inesperado');
      }
    });
  }

  private error(msg: string): void {
    this.mensajeError.set(msg);
    setTimeout(() => this.mensajeError.set(''), 3500);
  }
}
