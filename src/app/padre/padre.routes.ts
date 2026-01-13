import { Routes } from '@angular/router';

export const PADRE_ROUTES: Routes = [
  {
    path: 'inicio',
    loadComponent: () =>
      import('./components/inicio/inicio.component')
        .then(m => m.InicioPadreComponent)
  },
  {
    path: 'documentos',
    loadComponent: () =>
      import('./components/documentos/documentos.component')
        .then(m => m.DocumentosComponent)
  },
  {
    path: 'mis-hijos',
    loadComponent: () =>
      import('./components/mis-hijos/mis-hijos.component')
        .then(m => m.MisHijosComponent)
  },
  {
    path: 'notificaciones',
    loadComponent: () =>
      import('..//shared/notification/notification.component')
        .then(m => m.NotificationComponent)
  }
];
