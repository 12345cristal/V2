import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Router } from '@angular/router';
import { tap } from 'rxjs/operators';
import { environment } from '../../environments/environment';

export interface UserInToken {
  id: number;
  nombres: string;
  apellido_paterno: string;
  apellido_materno?: string | null;
  email: string;
  rol_id: number;
  rol_nombre?: string | null;
  permisos: string[];
}

export interface LoginResponse {
  token: {
    access_token: string;
    token_type: string;
  };
  user: UserInToken;
}
@Injectable({ providedIn: 'root' })
export class AuthService {

  private apiUrl = `${environment.apiBaseUrl}/auth`;
  private _user: UserInToken | null = null;

  constructor(
    private http: HttpClient,
    private router: Router
  ) {
    this.cargarUsuarioDeLocalStorage();
  }

  // ==============================
  // LOGIN
  // ==============================
  login(correo: string, contrasena: string) {
    return this.http
      .post<LoginResponse>(`${this.apiUrl}/login`, {
        correo,
        contrasena
      })
      .pipe(
        tap(res => {
          localStorage.setItem('token', res.token.access_token);
          localStorage.setItem('user', JSON.stringify(res.user));
          this._user = res.user;
        })
      );
  }

  // ==============================
  // LOGOUT
  // ==============================
  logout(): void {
    localStorage.clear();
    this._user = null;
    this.router.navigate(['/login']);
  }

  // ==============================
  // TOKEN
  // ==============================
  get token(): string | null {
    return localStorage.getItem('token');
  }

  isLoggedIn(): boolean {
    return !!this.token && !this.isTokenExpired();
  }

  // ==============================
  // USUARIO
  // ==============================
  get user(): UserInToken | null {
    return this._user;
  }

  // ==============================
  // JWT EXP
  // ==============================
  isTokenExpired(): boolean {
    const token = this.token;
    if (!token) return true;

    try {
      const payload = JSON.parse(atob(token.split('.')[1]));
      return payload.exp < Math.floor(Date.now() / 1000);
    } catch {
      return true;
    }
  }

  private cargarUsuarioDeLocalStorage(): void {
    const raw = localStorage.getItem('user');
    this._user = raw ? JSON.parse(raw) : null;
  }
}
