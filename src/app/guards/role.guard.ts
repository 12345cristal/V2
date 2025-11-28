import { inject } from '@angular/core';
import { CanMatchFn, Router } from '@angular/router';
import { AuthService } from '../../services/auth.service';

export const roleGuard: CanMatchFn = (route, segments) => {
  const auth = inject(AuthService);
  const router = inject(Router);

  const expected = route.data?.['role'] as string | string[] | undefined;
  const current = auth.getRol();

  if (!expected) return true;

  const allowed = Array.isArray(expected)
    ? expected.includes(current)
    : expected === current;

  if (!allowed) {
    router.navigate(['/']);   // o /login
    return false;
  }

  return true;
};
