import { Routes } from '@angular/router';

// Layout raíz del sistema
import { LayoutComponent } from '../shared/layout/layout';

// Páginas del terapeuta
import { PacientesComponent } from './pacientes/pacientes';
import { HorariosComponent } from './horarios/horarios';
import { Actividades } from './actividades/actividades';
import { PerfilComponent } from '../shared/perfil/perfil';
import { RecursosTerapeutaComponent } from './recursos/recursos-terapeuta';
import { InicioTerapeutaComponent } from './inicio/inicio';
import { RecomendacionPanelTerapeutaComponent } from './recomendacion-panel/recomendacion-panel';
import { TerapeutaRecomendacionesComponent } from './recomendaciones/recomendaciones';
import { AsistenciasTerapeutaComponent } from './asistencias/asistencias';

export const TERAPEUTA_ROUTES: Routes = [
  {
    path: '',
    component: LayoutComponent, // layout del terapeuta
    children: [
      { path: 'inicio', component: InicioTerapeutaComponent },
      { path: 'pacientes', component: PacientesComponent },
      { path: 'horarios', component: HorariosComponent },
      { path: 'actividades', component: Actividades },
      { path: 'asistencias', component: AsistenciasTerapeutaComponent },
      { 
        path: 'reportes', 
        loadComponent: () => import('./reportes/reportes').then(m => m.ReportesTerapeutaComponent)
      },
      { 
        path: 'mensajes', 
        loadComponent: () => import('./mensajes/mensajes').then(m => m.MensajesTerapeutaComponent)
      },
      { path: 'recursos', component: RecursosTerapeutaComponent },
      { path: 'recomendaciones', component: TerapeutaRecomendacionesComponent },
      { path: 'perfil', component: PerfilComponent },
      // Default
      { path: '', redirectTo: 'inicio', pathMatch: 'full' }
    ]
  }
];

