import { Routes } from '@angular/router';

import { Layout } from '../share/layout/layout';

// Páginas del terapeuta
import { Inicio } from '../coordinador/inicio/inicio';
import { Pacientes } from './pacientes/pacientes';
import { Horarios } from './horarios/horarios';
import { Actividades } from './actividades/actividades';
import { PerfilComponent } from '../share/perfil/perfil';

export const TERAPEUTA_ROUTES: Routes = [
  {
    path: '',
    component: Layout,
    children: [
      { path: 'inicio', component: Inicio },
      { path: 'pacientes', component: Pacientes },
      { path: 'horarios', component: Horarios },
      { path: 'actividades', component: Actividades },
      { path: 'perfil', component: PerfilComponent },

      // Ruta por defecto → inicio
      { path: '', redirectTo: 'inicio', pathMatch: 'full' }
    ]
  }
];
