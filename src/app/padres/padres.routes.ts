import { Routes } from '@angular/router';
import { LayoutComponent } from '../shared/layout/layout';

export const PADRES_ROUTES: Routes = [
  {
    path: '',
    component: LayoutComponent,
    children: [

      // ==============================
      // 1️⃣ INICIO (ÚNICO CON Component)
      // ==============================
      {
        path: 'inicio',
        loadComponent: () =>
          import('./inicio/inicio.component')
            .then(m => m.InicioComponent)
      },

      // ==============================
      // 2️⃣ MIS HIJOS
      // ==============================
      {
        path: 'mis-hijos',
        loadComponent: () =>
          import('./mis-hijos/mis-hijos')
            .then(m => m.MisHijos)
      },

      // ==============================
      // 3️⃣ SESIONES
      // ==============================
      {
        path: 'sesiones',
        loadComponent: () =>
          import('./sesiones/sesiones')
            .then(m => m.Sesiones)
      },

      // ==============================
      // 4️⃣ HISTORIAL TERAPÉUTICO
      // ==============================
      {
        path: 'historial-terapeutico',
        loadComponent: () =>
          import('./historial-terapeutico/historial-terapeutico')
            .then(m => m.HistorialTerapeutico)
      },

      // ==============================
      // 5️⃣ TAREAS
      // ==============================
      {
        path: 'tareas',
        loadComponent: () =>
          import('./tareas/tareas')
            .then(m => m.Tareas)
      },

      // ==============================
      // 6️⃣ PAGOS
      // ==============================
      {
        path: 'pagos',
        loadComponent: () =>
          import('./pagos-section/pagos-section')
            .then(m => m.PagosSection)
      },

      // ==============================
      // 7️⃣ DOCUMENTOS
      // ==============================
      {
        path: 'documentos',
        loadComponent: () =>
          import('./documentos-section/documentos-section')
            .then(m => m.DocumentosSection)
      },

      // ==============================
      // 8️⃣ RECURSOS
      // ==============================
      {
        path: 'recursos',
        loadComponent: () =>
          import('./recursos/recursos')
            .then(m => m.Recursos)
      },

      // ==============================
      // 9️⃣ MENSAJES
      // ==============================
      {
        path: 'mensajes',
        loadComponent: () =>
          import('./mensajes/mensajes')
            .then(m => m.Mensajes)
      },

      // ==============================
      // 🔔 10️⃣ NOTIFICACIONES
      // ==============================
      {
        path: 'notificaciones',
        loadComponent: () =>
          import('./notificaciones/notificaciones')
            .then(m => m.Notificaciones)
      },

      // ==============================
      // ⚙️ 11️⃣ PERFIL Y ACCESIBILIDAD
      // ==============================
      {
        path: 'perfil',
        loadComponent: () =>
          import('./perfil-accesibilidad/perfil-accesibilidad')
            .then(m => m.PerfilAccesibilidad)
      },

      // ==============================
      // RUTA POR DEFECTO
      // ==============================
      {
        path: '',
        redirectTo: 'inicio',
        pathMatch: 'full'
      }
    ]
  }
];
