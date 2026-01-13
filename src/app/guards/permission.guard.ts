// src/app/auth/permission.guard.ts
import { Injectable } from '@angular/core';
import { CanActivate, ActivatedRouteSnapshot, Router } from '@angular/router';
import { AuthService } from '../auth/auth.service';

@Injectable({ providedIn: 'root' })
export class PermissionGuard implements CanActivate {

  constructor(
    private auth: AuthService,
    private router: Router,
  ) {}

  canActivate(route: ActivatedRouteSnapshot): boolean {
    const requiredPerms = route.data['permisos'] as string[] | undefined;

    if (!this.auth.isLoggedIn()) {
      this.router.navigate(['/login']);
      return false;
    }

    if (requiredPerms && !this.auth.hasAnyPermission(requiredPerms)) {
      this.router.navigate(['/no-autorizado']);
      return false;
    }

    return true;
  }
}

