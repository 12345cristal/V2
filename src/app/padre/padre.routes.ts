import { Routes } from '@angular/router';

export const PADRE_ROUTES: Routes = [
  {
    path: '',
    children: [
      {
        path: 'inicio',
        loadComponent: () =>
          import('./componentes/inicio/inicio.component').then(
            (m) => m.InicioComponent
          ),
        data: { title: 'Inicio' }
      },
      {
        path: 'mis-hijos',
        loadComponent: () =>
          import('./componentes/mis-hijos/mis-hijos.component').then(
            (m) => m.MisHijosComponent
          ),
        data: { title: 'Mis Hijos' }
      },
      {
        path: 'sesiones',
        loadComponent: () =>
          import('./componentes/sesiones/sesiones.component').then(
            (m) => m.SesionesComponent
          ),
        data: { title: 'Sesiones' }
      },
      {
        path: 'historial',
        loadComponent: () =>
          import('./componentes/historial/historial.component').then(
            (m) => m.HistorialComponent
          ),
        data: { title: 'Historial' }
      },
      {
        path: 'tareas',
        loadComponent: () =>
          import('./componentes/tareas/tareas.component').then(
            (m) => m.TareasComponent
          ),
        data: { title: 'Tareas' }
      },
      {
        path: 'pagos',
        loadComponent: () =>
          import('./componentes/pagos/pagos.component').then(
            (m) => m.PagosComponent
          ),
        data: { title: 'Pagos' }
      },
      {
        path: 'documentos',
        loadComponent: () =>
          import('./componentes/documentos/documentos.component').then(
            (m) => m.DocumentosComponent
          ),
        data: { title: 'Documentos' }
      },
      {
        path: 'recursos',
        loadComponent: () =>
          import('./componentes/recursos/recursos.component').then(
            (m) => m.RecursosComponent
          ),
        data: { title: 'Recursos Recomendados' }
      },
      {
        path: 'notificaciones',
        loadComponent: () =>
          import(
            './componentes/notificaciones/notificaciones.component'
          ).then((m) => m.NotificacionesComponent),
        data: { title: 'Notificaciones' }
      },
      {
        path: 'perfil',
        loadComponent: () =>
          import('./componentes/perfil/perfil.component').then(
            (m) => m.PerfilComponent
          ),
        data: { title: 'Mi Perfil' }
      },
      {
        path: 'accesibilidad',
        loadComponent: () =>
          import('./componentes/accesibilidad/accesibilidad.component').then(
            (m) => m.AccesibilidadComponent
          ),
        data: { title: 'Accesibilidad' }
      },
      {
        path: '',
        redirectTo: 'inicio',
        pathMatch: 'full'
      }
    ]
  }
];
