import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Router } from '@angular/router';
import { tap } from 'rxjs/operators';
import { environment } from 'src/environments/environment';

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

  // ==========================================
  // LOGIN
  // ==========================================
  login(email: string, password: string) {
    return this.http
      .post<LoginResponse>(`${this.apiUrl}/login`, { email, password })
      .pipe(
        tap(res => {
          localStorage.setItem('token', res.token.access_token);
          localStorage.setItem('user', JSON.stringify(res.user));
          this._user = res.user;
        })
      );
  }

  // ==========================================
  // LOGOUT
  // ==========================================
  logout(): void {
    localStorage.removeItem('token');
    localStorage.removeItem('user');
    this._user = null;
    this.router.navigate(['/login']);
  }

  // ==========================================
  // TOKEN
  // ==========================================
  obtenerToken(): string | null {
    return localStorage.getItem('token');
  }

  get token(): string | null {
    return localStorage.getItem('token');
  }

  // ==========================================
  // ESTADO DE SESIÓN
  // ==========================================
  isLoggedIn(): boolean {
    return !!this.token && !this.isTokenExpired();
  }

  // ==========================================
  // USUARIO
  // ==========================================
  get user(): UserInToken | null {
    return this._user;
  }

  getUser(): UserInToken | null {
    return this._user;
  }

  // ==========================================
  // ROLES
  // ==========================================
  getRoleId(): number | null {
    return this._user?.rol_id ?? null;
  }

  getRoleName(): string | null {
    return this._user?.rol_nombre ?? null;
  }

  // ==========================================
  // PERMISOS
  // ==========================================
  hasPermission(permission: string): boolean {
    return this._user?.permisos.includes(permission) ?? false;
  }

  hasAnyPermission(required: string[]): boolean {
    if (!this._user) return false;
    return required.some(p => this._user!.permisos.includes(p));
  }

  // ==========================================
  // VALIDAR EXPIRACIÓN TOKEN JWT
  // ==========================================
  isTokenExpired(): boolean {
    const token = this.token;
    if (!token) return true;

    try {
      const payloadBase64 = token.split('.')[1];
      const payload = JSON.parse(atob(payloadBase64));
      if (!payload.exp) return true;

      const now = Math.floor(Date.now() / 1000);
      return payload.exp < now;
    } catch {
      return true;
    }
  }

  // ==========================================
  // CARGAR USUARIO DESDE LOCALSTORAGE
  // ==========================================
  private cargarUsuarioDeLocalStorage(): void {
    const raw = localStorage.getItem('user');
    this._user = raw ? JSON.parse(raw) as UserInToken : null;
  }
}

