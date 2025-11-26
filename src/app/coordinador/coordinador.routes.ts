import { Routes } from '@angular/router';

import { Citas } from './citas/citas';
import { Ninos } from './ninos/ninos';
import { Usuarios } from './usuarios/usuarios';
import { Terapias } from './terapias/terapias';
import { Perfil } from './perfil/perfil';
import { Configuracion } from './configuracion/configuracion';

import { Layout } from './layout/layout';

/* ==== IMPORTS DEL MÓDULO PERSONAL ==== */
import { PersonalListComponent } from './personal/personal-list/personal-list';
import { PersonalFormComponent } from './personal/personal-form/personal-form';


export const COORDINADOR_ROUTES: Routes = [
  {
    path: '',
    component: Layout,
    children: [

      /* ===============================
         🔵 RUTAS DEL MÓDULO PERSONAL
         =============================== */
      { path: 'personal', component: PersonalListComponent },
      { path: 'personal/nuevo', component: PersonalFormComponent },
      { path: 'personal/editar/:id', component: PersonalFormComponent },

      /* ===============================
         🔵 RUTAS EXISTENTES
         =============================== */
      { path: 'citas', component: Citas },
      { path: 'ninos', component: Ninos },
      { path: 'usuarios', component: Usuarios },
      { path: 'terapias', component: Terapias },
      { path: 'perfil', component: Perfil },
      { path: 'configuracion', component: Configuracion },

      /* Ruta por defecto dentro del layout */
      { path: '', redirectTo: 'citas', pathMatch: 'full' },
    ],
  },
];
