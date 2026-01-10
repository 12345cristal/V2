// src/app/app.routes.ts
import { Routes } from '@angular/router';

import { HEADER_ROUTES } from './pages/header_routes';

// Landing
import { LandingPageComponent } from './pages/landing/landing';

// Guards nuevos
import { AuthGuard } from './guards/auth.guard';
import { PermissionGuard } from './guards/permission.guard';
import { RoleGuard } from './guards/role.guard';

export const routes: Routes = [

  // =======================================
  // 🏠 RUTA RAÍZ
  // =======================================
  {
    path: '',
    redirectTo: 'inicio',
    pathMatch: 'full'
  },

  // =======================================
  // 🌐 LANDING PAGE PÚBLICA
  // =======================================
  {
    path: 'inicio',
    component: LandingPageComponent
  },

  // =======================================
  // 🌐 RUTAS PÚBLICAS (header)
  // =======================================
  ...HEADER_ROUTES,


  // =======================================
  // 👤 LOGIN (si lo quieres)
  // =======================================
  {
    path: 'login',
    loadComponent: () =>
      import('./pages/login/login')
        .then(m => m.LoginComponent)
  },

  // =======================================
  // 👥 PERFIL DE USUARIO
  // =======================================
  {
    path: 'perfil',
    canActivate: [AuthGuard],
    loadComponent: () =>
      import('./perfil/perfil')
        .then(m => m.PerfilComponent)
  },

  // =======================================
  // 🟦 COORDINADOR / USUARIOS (ruta directa)
  // SOLO SI tiene permisos `usuarios:listar`
  // =======================================
  {
    path: 'coordinador/usuarios',
    canActivate: [AuthGuard, PermissionGuard],
    data: {
      permisos: ['usuarios:listar']    // PERMISO REAL DE TU BD
    },
    loadComponent: () =>
      import('./coordinador/usuarios/usuarios')
        .then(m => m.UsuariosComponent)
  },


  // =======================================
  // 🟦 COORDINADOR (lazy-load completo)
  // =======================================
  {
    path: 'coordinador',
    canActivate: [AuthGuard, RoleGuard],
    data: {
      roles: [1, 2] // ADMINISTRADOR=1, COORDINADOR=2
    },
    loadChildren: () =>
      import('./coordinador/coordinador.routes')
        .then(m => m.COORDINADOR_ROUTES)
  },


  // =======================================
  // 🟩 TERAPEUTA
  // =======================================
  {
    path: 'terapeuta',
    canActivate: [AuthGuard, RoleGuard],
    data: {
      roles: [3] // Terapeuta
    },
    loadChildren: () =>
      import('./terapeuta/terapeuta.routes')
        .then(m => m.TERAPEUTA_ROUTES)
  },


  // =======================================
  // 🟨 PADRE
  // =======================================
  {
    path: 'padre',
    canActivate: [AuthGuard, RoleGuard],
    data: {
      roles: [4] // Padre
    },
    loadChildren: () =>
      import('./padre/padre.routes')
        .then(m => m.PADRE_ROUTES)
  },


  // =======================================
  // ❌ 404
  // =======================================
  {
    path: '**',
    loadComponent: () =>
      import('./error/error-404')
        .then(m => m.Error404Component)
  }
];
