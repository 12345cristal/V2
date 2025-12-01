import { Routes } from '@angular/router';

// Layout raíz del sistema
import { Layout } from '../shared/layout/layout';

// Páginas del terapeuta
import { PacientesComponent } from './pacientes/pacientes';
import { HorariosComponent } from './horarios/horarios';
import { Actividades } from './actividades/actividades';
import { PerfilComponent } from '../shared/perfil/perfil';
import { RecursosTerapeutaComponent } from './recursos/recursos-terapeuta';
import { InicioTerapeutaComponent } from './inicio/inicio';
export const TERAPEUTA_ROUTES: Routes = [
  {
    path: '',
    component: Layout, // layout del terapeuta
    children: [
      { path: 'pacientes', component: PacientesComponent },
      { path: 'horarios', component: HorariosComponent },
      { path: 'actividades', component: Actividades },
      { path: 'perfil', component: PerfilComponent },
      { path: 'recursos', component: RecursosTerapeutaComponent },
{path: 'inicio', component: InicioTerapeutaComponent },
      // Default
      { path: '', redirectTo: 'pacientes', pathMatch: 'full' }
    ]
  }
];

