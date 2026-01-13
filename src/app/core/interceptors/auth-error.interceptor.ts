import { Injectable } from '@angular/core';
import { CanActivate, CanMatch, Router } from '@angular/router';
import { AuthService } from '../../auth/auth.service';

@Injectable({ providedIn: 'root' })
export class AuthGuard implements CanActivate, CanMatch {

  constructor(
    private auth: AuthService,
    private router: Router
  ) {}

  private checkAuth(): boolean {

    const token = this.auth.token;

    if (!token) {
      this.router.navigate(['/login']);
      return false;
    }

    // OPCIONAL: Validar expiración
    const isExpired = this.auth.isTokenExpired();
    if (isExpired) {
      this.auth.logout();
      return false;
    }

    return true;
  }

  canActivate(): boolean {
    return this.checkAuth();
  }

  canMatch(): boolean {
    return this.checkAuth();
  }
}



