// src/app/auth/auth.service.ts
import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { tap } from 'rxjs/operators';

import { environment } from '../enviroment/environment';

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

  constructor(private http: HttpClient) {}

  login(email: string, password: string) {
    return this.http.post<LoginResponse>(`${this.apiUrl}/login`, { email, password })
      .pipe(
        tap(res => {
          localStorage.setItem('token', res.token.access_token);
          localStorage.setItem('user', JSON.stringify(res.user));
        })
      );
  }

  logout(): void {
    localStorage.removeItem('token');
    localStorage.removeItem('user');
  }

  getToken(): string | null {
    return localStorage.getItem('token');
  }

  getUser(): UserInToken | null {
    const raw = localStorage.getItem('user');
    return raw ? JSON.parse(raw) as UserInToken : null;
  }

  isLoggedIn(): boolean {
    return !!this.getToken();
  }

  hasPermission(permiso: string): boolean {
    const user = this.getUser();
    if (!user) return false;
    return user.permisos?.includes(permiso);
  }

  hasAnyPermission(permisos: string[]): boolean {
    const user = this.getUser();
    if (!user) return false;
    return permisos.some(p => user.permisos?.includes(p));
  }
}
