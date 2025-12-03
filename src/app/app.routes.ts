import { Routes } from '@angular/router';

import { HEADER_ROUTES } from './pages/header_routes';

// Landing real
import { LandingPageComponent } from './pages/landing/landing';

// Guards
import { AuthGuard } from './guards/auth.guard';
import { PermissionGuard } from './guards/permission.guard';

export const routes: Routes = [

  // 🏠 Ruta inicial
  {
    path: '',
    redirectTo: 'inicio',
    pathMatch: 'full'
  },

  // 🏠 Landing Page real
  {
    path: 'inicio',
    component: LandingPageComponent
  },

  // 🌐 Rutas públicas del header
  ...HEADER_ROUTES,

  // 🟦 COORDINADOR / USUARIOS (ruta protegida independiente)
  // DEBE IR *ANTES* del módulo lazy de coordinador
  {
    path: 'coordinador/usuarios',
    canActivate: [AuthGuard, PermissionGuard],
    data: {
      permisos: ['usuarios:ver']  // este permiso viene de la BD
    },
    loadComponent: () =>
      import('./coordinador/usuarios/usuarios')
        .then(m => m.UsuariosComponent)
  },

  // 🟦 COORDINADOR (lazy-loading)
  {
    path: 'coordinador',
    canActivate: [AuthGuard], // protección general del módulo
    loadChildren: () =>
      import('./coordinador/coordinador.routes')
        .then(m => m.COORDINADOR_ROUTES),
  },

  // 🟩 TERAPEUTA (lazy-loading)
  {
    path: 'terapeuta',
    canActivate: [AuthGuard],
    loadChildren: () =>
      import('./terapeuta/terapeuta.routes')
        .then(m => m.TERAPEUTA_ROUTES),
  },

  // 🟨 PADRE (lazy-loading)
  {
    path: 'padre',
    canActivate: [AuthGuard],
    loadChildren: () =>
      import('./padre/padre.routes')
        .then(m => m.PADRE_ROUTES),
  },

  // 🔴 404 – Página no encontrada
  {
    path: '**',
    loadComponent: () =>
      import('./error/error-404')
        .then(m => m.Error404Component)
  }
];
