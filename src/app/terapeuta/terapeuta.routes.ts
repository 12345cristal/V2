import { Routes } from '@angular/router';

// Layout raíz
import { LayoutComponent } from '../shared/layout/layout';

// Páginas terapeuta
import { InicioTerapeutaComponent } from './inicio/inicio';
import { PacientesComponent } from './pacientes/pacientes';
import { HorariosComponent } from './horarios/horarios';
import { Actividades } from './actividades/actividades';
import { AsistenciasTerapeutaComponent } from './asistencias/asistencias';
import { RecursosTerapeutaComponent } from './recursos/recursos-terapeuta';
import { TerapeutaRecomendacionesComponent } from './recomendaciones/recomendaciones';
import { PerfilComponent } from '../shared/perfil/perfil';

export const TERAPEUTA_ROUTES: Routes = [
  {
    path: '',
    component: LayoutComponent,
    children: [

      // ===== PRINCIPAL =====
      { path: 'inicio', component: InicioTerapeutaComponent },

      // ===== MI TRABAJO =====
      { path: 'pacientes', component: PacientesComponent },
      { path: 'horarios', component: HorariosComponent },
      { path: 'actividades', component: Actividades },
      { path: 'asistencias', component: AsistenciasTerapeutaComponent },

      // ===== REPORTES =====
      {
        path: 'reportes',
        loadComponent: () =>
          import('./reportes/reportes')
            .then(m => m.ReportesTerapeutaComponent),
      },

      // ===== MENSAJES (COMPARTIDO) =====
      {
        path: 'mensajes',
        loadComponent: () =>
          import('../shared/mensajes/mensajes.component')
            .then(m => m.MensajesComponent),
      },

      // ===== RECURSOS =====
      { path: 'recursos', component: RecursosTerapeutaComponent },
      { path: 'recomendaciones', component: TerapeutaRecomendacionesComponent },

      // ===== CUENTA =====
      { path: 'perfil', component: PerfilComponent },

      // ===== DEFAULT =====
      { path: '', redirectTo: 'inicio', pathMatch: 'full' },
    ],
  },
];

