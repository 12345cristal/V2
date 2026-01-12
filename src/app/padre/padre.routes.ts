import { Routes } from '@angular/router';

export const PADRE_ROUTES: Routes = [
  {
    path: 'inicio',
    loadComponent: () =>
      import('./inicio/inicio.component')
        .then(c => c.InicioPadreComponent),
  },
  {
    path: 'mis-hijos',
    loadComponent: () =>
      import('./mis-hijos/mis-hijos.component')
        .then(c => c.MisHijosComponent),
  },
  {
    path: 'sesiones',
    loadComponent: () =>
      import('./sesiones/sesiones.component')
        .then(c => c.SesionesComponent),
  },
  {
    path: 'historial-terapeutico',
    loadComponent: () =>
      import('./historial/historial.component')
        .then(c => c.HistorialComponent),
  },
  {
    path: 'tareas',
    loadComponent: () =>
      import('./tareas/tareas.component')
        .then(c => c.TareasComponent),
  },
  {
    path: 'pagos',
    loadComponent: () =>
      import('./pagos/pagos.component')
        .then(c => c.PagosComponent),
  },
  {
    path: 'documentos',
    loadComponent: () =>
      import('./documentos/documentos.component')
        .then(c => c.DocumentosComponent),
  },
  {
    path: 'recursos',
    loadComponent: () =>
      import('./recursos/recursos.component')
        .then(c => c.RecursosComponent),
  },
  {
    path: 'mensajes',
    loadComponent: () =>
      import('./mensajes/mensajes.component')
        .then(c => c.MensajesComponent),
  },
  {
    path: 'notificaciones',
    loadComponent: () =>
      import('./notificaciones/notificaciones.component')
        .then(c => c.NotificacionesComponent),
  },
  {
    path: 'perfil',
    loadComponent: () =>
      import('./perfil/perfil.component')
        .then(c => c.PerfilPadreComponent),
  },
  {
    path: 'accesibilidad',
    loadComponent: () =>
      import('./accesibilidad/accesibilidad.component')
        .then(c => c.AccesibilidadComponent),
  },
  {
    path: '',
    redirectTo: 'inicio',
    pathMatch: 'full',
  }
];
