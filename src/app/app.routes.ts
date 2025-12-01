import { Routes } from '@angular/router';
import { HEADER_ROUTES } from './pages/header_routes';

export const routes: Routes = [

  // =====================================
  // 🏠 RUTA INICIAL (Landing por defecto)
  // =====================================
  {
    path: '',
    redirectTo: 'inicio',   // Página inicial
    pathMatch: 'full'
  },

  // =====================================
  // 🌐 RUTAS DEL HEADER (páginas públicas)
  // =====================================
  ...HEADER_ROUTES,

  // =====================================
  // 🟦 COORDINADOR (lazy-loading)
  // =====================================
  {
    path: 'coordinador',
    loadChildren: () =>
      import('./coordinador/coordinador.routes')
        .then(m => m.COORDINADOR_ROUTES),
  },

  // =====================================
  // 🟨 PADRE (lazy-loading)
  // =====================================
  {
    path: 'padre',
    loadChildren: () =>
      import('./padre/padre.routes')
        .then(m => m.PADRE_ROUTES),
  },
 {
    path: 'terapeuta',
    // canActivate: [AuthGuard],
    loadChildren: () =>
      import('./terapeuta/terapeuta.routes')
        .then(m => m.TERAPEUTA_ROUTES),
  },

  // =====================================
  // 🔴 RUTA NO ENCONTRADA (404)
  // =====================================
  {
    path: '**',
    redirectTo: 'inicio'
  }
];



