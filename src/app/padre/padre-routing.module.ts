import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { LayoutComponent } from '../shared/layout/layout';

/**
 * Rutas del módulo Padre
 * Define las 11 secciones principales del dashboard
 */
const routes: Routes = [
  {
    path: '',
    component: LayoutComponent,
    children: [
      // ==============================
      // 📊 1. DASHBOARD / INICIO
      // ==============================
      {
        path: 'inicio',
        loadComponent: () =>
          import('./inicio/inicio')
            .then(m => m.InicioPadreComponent),
        data: { title: 'Dashboard' }
      },

      // ==============================
      // 👶 2. MIS HIJOS
      // ==============================
      {
        path: 'info-nino',
        loadComponent: () =>
          import('./info-nino/info-nino')
            .then(m => m.InfoNinoComponent),
        data: { title: 'Mis Hijos' }
      },
      {
        path: 'info-nino/:id',
        loadComponent: () =>
          import('./info-nino/info-nino')
            .then(m => m.InfoNinoComponent),
        data: { title: 'Información del Niño' }
      },

      // ==============================
      // 📅 3. SESIONES
      // ==============================
      {
        path: 'sesiones',
        loadComponent: () =>
          import('./inicio/inicio')
            .then(m => m.InicioPadreComponent),
        data: { title: 'Sesiones', section: 'sesiones' }
      },
      {
        path: 'sesiones/:id',
        loadComponent: () =>
          import('./inicio/inicio')
            .then(m => m.InicioPadreComponent),
        data: { title: 'Detalle de Sesión', section: 'sesion-detalle' }
      },

      // ==============================
      // 📈 4. HISTORIAL TERAPÉUTICO
      // ==============================
      {
        path: 'historial',
        loadComponent: () =>
          import('./inicio/inicio')
            .then(m => m.InicioPadreComponent),
        data: { title: 'Historial Terapéutico', section: 'historial' }
      },

      // ==============================
      // ✅ 5. TAREAS / ACTIVIDADES
      // ==============================
      {
        path: 'actividades',
        loadComponent: () =>
          import('./actividades/actividades')
            .then(m => m.PadreActividadesComponent),
        data: { title: 'Tareas y Actividades' }
      },
      {
        path: 'actividades/:id',
        loadComponent: () =>
          import('./actividades/actividad-detalle/actividad-detalle')
            .then(m => m.ActividadDetalleComponent),
        data: { title: 'Detalle de Actividad' }
      },

      // ==============================
      // 💳 6. PAGOS
      // ==============================
      {
        path: 'pagos',
        loadComponent: () =>
          import('./inicio/inicio')
            .then(m => m.InicioPadreComponent),
        data: { title: 'Pagos y Facturación', section: 'pagos' }
      },
      {
        path: 'pagos/historial',
        loadComponent: () =>
          import('./inicio/inicio')
            .then(m => m.InicioPadreComponent),
        data: { title: 'Historial de Pagos', section: 'pagos-historial' }
      },

      // ==============================
      // 📄 7. DOCUMENTOS
      // ==============================
      {
        path: 'documentos',
        loadComponent: () =>
          import('./documentos/documentos')
            .then(m => m.default),
        data: { title: 'Documentos' }
      },
      {
        path: 'documentos/lista-padre',
        loadComponent: () =>
          import('./documentos/docs-list-padre/docs-list-padre')
            .then(m => m.default),
        data: { title: 'Mis Documentos' }
      },
      {
        path: 'documentos/lista-terapeuta',
        loadComponent: () =>
          import('./documentos/docs-list-terapeuta/docs-list-terapeuta')
            .then(m => m.default),
        data: { title: 'Documentos del Terapeuta' }
      },
      {
        path: 'documentos/subir',
        loadComponent: () =>
          import('./documentos/upload-doc-padre/upload-doc-padre')
            .then(m => m.default),
        data: { title: 'Subir Documento' }
      },

      // ==============================
      // 📚 8. RECURSOS EDUCATIVOS
      // ==============================
      {
        path: 'recursos',
        loadComponent: () =>
          import('./inicio/inicio')
            .then(m => m.InicioPadreComponent),
        data: { title: 'Recursos Educativos', section: 'recursos' }
      },
      {
        path: 'recursos/:id',
        loadComponent: () =>
          import('./inicio/inicio')
            .then(m => m.InicioPadreComponent),
        data: { title: 'Detalle de Recurso', section: 'recurso-detalle' }
      },

      // ==============================
      // 💬 9. MENSAJES
      // ==============================
      {
        path: 'mensajes',
        loadComponent: () =>
          import('./inicio/inicio')
            .then(m => m.InicioPadreComponent),
        data: { title: 'Mensajes', section: 'mensajes' }
      },
      {
        path: 'mensajes/:chatId',
        loadComponent: () =>
          import('./inicio/inicio')
            .then(m => m.InicioPadreComponent),
        data: { title: 'Chat', section: 'chat' }
      },

      // ==============================
      // 🔔 10. NOTIFICACIONES
      // ==============================
      {
        path: 'notificaciones',
        loadComponent: () =>
          import('./inicio/inicio')
            .then(m => m.InicioPadreComponent),
        data: { title: 'Notificaciones', section: 'notificaciones' }
      },

      // ==============================
      // 👤 11. PERFIL Y CONFIGURACIÓN
      // ==============================
      {
        path: 'perfil',
        loadComponent: () =>
          import('../shared/perfil/perfil')
            .then(m => m.PerfilComponent),
        data: { title: 'Mi Perfil' }
      },
      {
        path: 'perfil/accesibilidad',
        loadComponent: () =>
          import('../shared/perfil/perfil')
            .then(m => m.PerfilComponent),
        data: { title: 'Accesibilidad', section: 'accesibilidad' }
      },
      {
        path: 'perfil/preferencias',
        loadComponent: () =>
          import('../shared/perfil/perfil')
            .then(m => m.PerfilComponent),
        data: { title: 'Preferencias', section: 'preferencias' }
      },

      // ==============================
      // 🔄 TERAPIAS Y RECOMENDACIONES
      // ==============================
      {
        path: 'terapias',
        loadComponent: () =>
          import('./terapias/terapias')
            .then(m => m.TerapiasComponent),
        data: { title: 'Terapias Asignadas' }
      },
      {
        path: 'recomendaciones',
        loadComponent: () =>
          import('./recomendaciones/recomendaciones')
            .then(m => m.RecomendacionesPadreComponent),
        data: { title: 'Recomendaciones' }
      },

      // ==============================
      // 📌 RUTA POR DEFECTO
      // ==============================
      {
        path: '',
        redirectTo: 'inicio',
        pathMatch: 'full'
      }
    ]
  }
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class PadreRoutingModule { }
