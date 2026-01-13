// src/app/auth/auth.service.ts
import { Injectable, signal } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, tap } from 'rxjs';
import { environment } from '../../environments/environment';
import { AuthUser, LoginResponse } from '../interfaces/auth-response.interface';

export interface LoginRequest {
  email: string;
  password: string;
}

@Injectable({ providedIn: 'root' })
export class AuthService {
  private readonly TOKEN_KEY = 'token';
  private readonly USER_KEY = 'user';

  private readonly _user = signal<AuthUser | null>(null);
  readonly user = this._user.asReadonly();

  constructor(private http: HttpClient) {
    const stored = localStorage.getItem(this.USER_KEY);
    if (stored) this._user.set(JSON.parse(stored));
  }

  // ===========================
  // AUTH
  // ===========================
  login(email: string, password: string): Observable<LoginResponse> {
    return this.http
      .post<LoginResponse>(`${environment.apiBaseUrl}/auth/login`, { email, password })
      .pipe(
        tap(res => {
          localStorage.setItem(this.TOKEN_KEY, res.access_token);
          localStorage.setItem(this.USER_KEY, JSON.stringify(res.user));
          this._user.set(res.user);
        })
      );
  }

  logout(): void {
    localStorage.removeItem(this.TOKEN_KEY);
    localStorage.removeItem(this.USER_KEY);
    this._user.set(null);
    location.href = '/login';
  }

  // ===========================
  // HELPERS
  // ===========================
  isLoggedIn(): boolean {
    return !!localStorage.getItem(this.TOKEN_KEY);
  }

  obtenerToken(): string | null {
    return localStorage.getItem(this.TOKEN_KEY);
  }

  getRoleId(): number | null {
    return this._user()?.rol_id ?? null;
  }

  hasAnyPermission(perms: string[]): boolean {
    const user: any = this._user();
    if (!user?.permisos) return false;
    return perms.some(p => user.permisos.includes(p));
  }
}
