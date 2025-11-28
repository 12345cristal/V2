import { Routes } from '@angular/router';

export const routes: Routes = [

  // ========= COORDINADOR =========
  {
    path: 'coordinador',
    loadChildren: () =>
      import('./coordinador/coordinador.routes')
        .then(m => m.COORDINADOR_ROUTES),
  },

  // ========= TERAPEUTA =========
  {
    path: 'terapeuta',
    loadChildren: () =>
      import('./terapeuta/terapeuta.routes')
        .then(m => m.TERAPEUTA_ROUTES),
  },

  // ========= PADRE (si aplica) =========
  // {
  //   path: 'padre',
  //   loadChildren: () =>
  //     import('./padre/padre.routes')
  //       .then(m => m.PADRE_ROUTES),
  // },

  // ========= RUTA RAÍZ =========
  { path: '', redirectTo: 'coordinador', pathMatch: 'full' },

  // ========= RUTA NO ENCONTRADA =========
  // { path: '**', redirectTo: 'coordinador' }
];
