import { Routes } from '@angular/router';
import { HEADER_ROUTES } from './pages/header_routes';

// Importar el Landing (inicio verdadero)
import { LandingPageComponent } from './pages/landing/landing';

export const routes: Routes = [

  // =====================================
  // 🏠 RUTA INICIAL (Landing por defecto)
  // =====================================
  {
    path: '',
    redirectTo: 'inicio',
    pathMatch: 'full'
  },

  // =====================================
  // 🏠 RUTA REAL DEL LANDING
  // =====================================
  {
    path: 'inicio',
    component: LandingPageComponent
  },

  // =====================================
  // 🌐 RUTAS DEL HEADER (públicas)
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
  // 🟩 TERAPEUTA (lazy-loading)
  // =====================================
  {
    path: 'terapeuta',
    loadChildren: () =>
      import('./terapeuta/terapeuta.routes')
        .then(m => m.TERAPEUTA_ROUTES),
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

  // =====================================
  // 🔴 404 – RUTA NO ENCONTRADA
  // =====================================
  {
    path: '**',
    redirectTo: 'inicio'
  }
];
