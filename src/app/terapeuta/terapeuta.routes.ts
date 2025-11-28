import { Routes } from '@angular/router';

// Layout raíz del sistema
import { Layout } from '../share/layout/layout';

// Páginas del terapeuta
import { PacientesComponent } from './pacientes/pacientes';
import { HorariosComponent } from './horarios/horarios';
import { Actividades } from './actividades/actividades';
import { PerfilComponent } from '../share/perfil/perfil';

// Si tienes inicio para terapeuta, debe estar aquí
// import { InicioTerapeutaComponent } from './inicio/inicio';

export const TERAPEUTA_ROUTES: Routes = [
  {
    path: '',
    component: Layout,
    children: [
      // { path: 'inicio', component: InicioTerapeutaComponent },

      { path: 'pacientes', component: PacientesComponent },
      { path: 'horarios', component: HorariosComponent },
      { path: 'actividades', component: Actividades},
      { path: 'perfil', component: PerfilComponent },

      // Ruta por defecto
      { path: '', redirectTo: 'pacientes', pathMatch: 'full' }
    ]
  }
];
