import { Routes } from '@angular/router';
import { LayoutComponent } from '../shared/layout/layout';
import { PerfilComponent } from '../shared/perfil/perfil';

export const TERAPEUTA_ROUTES: Routes = [
  {
    path: '',
    component: LayoutComponent,
    children: [
      // =========================
      // INICIO
      // =========================
      {
        path: 'inicio',
        loadComponent: () =>
          import('./inicio/inicio').then(m => m.InicioTerapeuta),
      },

      // =========================
      // PACIENTES
      // =========================
      {
        path: 'pacientes',
        loadComponent: () =>
          import('./pacientes/pacientes').then(m => m.PacientesComponent),
      },

      // =========================
      // HORARIO
      // =========================
      {
        path: 'horarios',
        loadComponent: () =>
          import('./horarios/horarios').then(m => m.HorarioPage),
      },

      // =========================
      // ACTIVIDADES / TAREAS
      // =========================
      {
        path: 'actividades',
        loadComponent: () =>
          import('./actividades/actividades').then(m => m.Actividades),
      },
      {
        path: 'actividades/nino/:ninoId',
        loadComponent: () =>
          import('./tareas/tareas-nino').then(m => m.TareasNino),
      },

      // =========================
      // ASISTENCIAS / SESIONES
      // =========================
      {
        path: 'asistencias',
        loadComponent: () =>
          import('./asistencias/asistencias').then(m => m.AsistenciasPage),
      },
      {
        path: 'asistencias/nino/:ninoId',
        loadComponent: () =>
          import('./sesiones/sesiones').then(m => m.SesionesNinoPage),
      },

      // =========================
      // REPORTES
      // =========================
      {
        path: 'reportes',
        loadComponent: () =>
          import('./reportes/reportes').then(m => m.ReportesPage),
      },

      // =========================
      // RECURSOS
      // =========================
      {
        path: 'recursos',
        loadComponent: () =>
          import('./recursos/recursos-terapeuta').then(m => m.RecursosPage),
      },

      // =========================
      // RECOMENDACIONES
      // =========================
      {
        path: 'recomendaciones',
        loadComponent: () =>
          import('./recomendaciones/recomendaciones')
            .then(m => m.TerapeutaRecomendacionesComponent),
      },

      // =========================
      // PERFIL
      // =========================
      {
        path: 'perfil',
        component: PerfilComponent,
      },

      // =========================
      // DEFAULT
      // =========================
      {
        path: '',
        redirectTo: 'inicio',
        pathMatch: 'full',
      },
    ],
  },
];
