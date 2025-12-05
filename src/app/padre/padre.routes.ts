// src/app/padre/padre.routes.ts
import { Routes } from '@angular/router';
import { LayoutComponent } from '../shared/layout/layout';

export const PADRE_ROUTES: Routes = [
  {
    path: '',
    component: LayoutComponent,

    children: [

      // ==============================
      // 📌 INICIO
      // ==============================
      {
        path: 'inicio',
        loadComponent: () =>
          import('./inicio/inicio')
            .then(m => m.InicioPadreComponent)
      },

      // ==============================
      // 📌 INFORMACIÓN DEL NIÑO
      // ==============================
      {
        path: 'info-nino',
        loadComponent: () =>
          import('./info-nino/info-nino')
            .then(m => m.InfoNinoComponent)
      },

      // ==============================
      // 📌 TERAPIAS ASIGNADAS
      // ==============================
      {
        path: 'terapias',
        loadComponent: () =>
          import('./terapias/terapias')
            .then(m => m.TerapiasComponent)
      },

      // ==============================
      // 📌 ACTIVIDADES — LISTADO
      // ==============================
      {
        path: 'actividades',
        loadComponent: () =>
          import('./actividades/actividades')
            .then(m => m.PadreActividadesComponent)
      },

      // ==============================
      // 📌 ACTIVIDADES — DETALLE
      // ==============================
      {
        path: 'actividades/:id',
        loadComponent: () =>
          import('./actividades/actividad-detalle/actividad-detalle')
            .then(m => m.ActividadDetalleComponent)
      },

      // ==============================
      // 📌 DOCUMENTOS — PANEL PRINCIPAL
      // ==============================
      {
        path: 'documentos',
        loadComponent: () =>
          import('./documentos/documentos')
            .then(m => m.default)
      },

      // ==============================
      // 📌 DOCUMENTOS — LISTA PADRE
      // ==============================
      {
        path: 'documentos/lista-padre',
        loadComponent: () =>
          import('./documentos/docs-list-padre/docs-list-padre')
            .then(m => m.default)
      },

      // ==============================
      // 📌 DOCUMENTOS — LISTA TERAPEUTA
      // ==============================
      {
        path: 'documentos/lista-terapeuta',
        loadComponent: () =>
          import('./documentos/docs-list-terapeuta/docs-list-terapeuta')
            .then(m => m.default)
      },

      // ==============================
      // 📌 DOCUMENTOS — SUBIR DOCUMENTO
      // ==============================
      {
        path: 'documentos/subir',
        loadComponent: () =>
          import('./documentos/upload-doc-padre/upload-doc-padre')
            .then(m => m.default)
      },

      // ==============================
      // 📌 RECOMENDACIONES
      // ==============================
   {
  path: 'recomendaciones',
  loadComponent: () =>
    import('./recomendaciones/recomendaciones')
      .then(m => m.RecomendacionesPadreComponent)
},

      // ==============================
      // 📌 PERFIL
      // ==============================
      {
        path: 'perfil',
        loadComponent: () =>
          import('../shared/perfil/perfil')
            .then(m => m.PerfilComponent)
      },

      // ==============================
      // 📌 RUTA POR DEFECTO
      // ==============================
      { path: '', redirectTo: 'inicio', pathMatch: 'full' }
    ]
  }
];
