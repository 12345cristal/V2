import { Routes } from '@angular/router';

import { Citas } from './citas/citas';
import { Personal } from './personal/personal';
import { Ninos } from './ninos/ninos';
import { Usuarios } from './usuarios/usuarios';
import { Terapias } from './terapias/terapias';
import { Perfil } from './perfil/perfil';
import { Configuracion } from './configuracion/configuracion';

import { Layout } from './layout/layout';

export const COORDINADOR_ROUTES: Routes = [
  {
    path: '',
    component: Layout,
    children: [
      { path: 'citas', component: Citas },
      { path: 'personal', component: Personal },
      { path: 'ninos', component: Ninos },
      { path: 'usuarios', component: Usuarios },
      { path: 'terapias', component: Terapias },
      { path: 'perfil', component: Perfil },
      { path: 'configuracion', component: Configuracion },

      // Ruta por defecto dentro del layout
      { path: '', redirectTo: 'citas', pathMatch: 'full' },
    ],
  },
];
