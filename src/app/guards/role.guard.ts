import { Injectable } from '@angular/core';
import { CanActivate, ActivatedRouteSnapshot, Router } from '@angular/router';
import { AuthService } from '../auth/auth.service';

@Injectable({ providedIn: 'root' })
export class RoleGuard implements CanActivate {

  constructor(
    private auth: AuthService,
    private router: Router
  ) {}

  canActivate(route: ActivatedRouteSnapshot): boolean {

    const roles = route.data['roles'] as number[] | undefined;
    const userRole = this.auth.getRoleId();

    if (!this.auth.isLoggedIn()) {
      this.router.navigate(['/login']);
      return false;
    }

    if (roles && !roles.includes(userRole!)) {
      this.router.navigate(['/no-autorizado']);
      return false;
    }

    return true;
  }
}
