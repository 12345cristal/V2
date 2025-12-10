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

export const TERAPEUTA_ROUTES: Routes = [
  {
    path: '',
    component: LayoutComponent, // layout del terapeuta
    children: [
      { path: 'pacientes', component: PacientesComponent },
      { path: 'horarios', component: HorariosComponent },
      { path: 'actividades', component: Actividades },
      { path: 'perfil', component: PerfilComponent },
      { path: 'recursos', component: RecursosTerapeutaComponent },
      { path: 'inicio', component: InicioTerapeutaComponent },
      { path: 'recomendaciones', component: TerapeutaRecomendacionesComponent },
      // Default
      { path: '', redirectTo: 'inicio', pathMatch: 'full' }
    ]
  }
];

