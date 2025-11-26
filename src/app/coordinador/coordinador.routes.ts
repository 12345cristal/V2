import { Routes } from '@angular/router';

/* ==== IMPORTS DEL MÓDULO COORDINADOR ==== */

import { Citas } from './citas/citas';
import { Ninos } from './ninos/ninos/ninos';
import { NinoForm } from './ninos/nino-form/nino-form';
import { Usuarios } from './usuarios/usuarios';
import { Terapias } from './terapias/terapias';
import { Perfil } from './perfil/perfil';
import { Configuracion } from './configuracion/configuracion';

import { Layout } from './layout/layout';

/* ==== IMPORTS DEL MÓDULO PERSONAL ==== */
import { PersonalListComponent } from './personal/personal-list/personal-list';
import { PersonalFormComponent } from './personal/personal-form/personal-form';
import { PersonalDetalleComponent } from './personal/personal-detalle/personal-detalle';
import { PersonalHorariosComponent } from './personal/personal-horarios/personal-horarios';


export const COORDINADOR_ROUTES: Routes = [
  {
    path: '',
    component: Layout,
    children: [

      /* =======================================
         🔵 MÓDULO PERSONAL
         ======================================= */
      { path: 'personal', component: PersonalListComponent },
      { path: 'personal/nuevo', component: PersonalFormComponent },
      { path: 'personal/editar/:id', component: PersonalFormComponent },
      { path: 'personal/detalle/:id', component: PersonalDetalleComponent },
      { path: 'personal/horarios/:id', component: PersonalHorariosComponent },


      /* =======================================
         🟣 MÓDULO NIÑOS (COMPLETO)
         ======================================= */

      // LISTA PRINCIPAL
      { path: 'ninos', component: Ninos },

      // NUEVO NIÑO
      { path: 'ninos/nuevo', component: NinoForm },

      // VER PERFIL DEL NIÑO (usa el mismo form por ahora)
      { path: 'ninos/:id', component: NinoForm },

      // EDITAR NIÑO
      { path: 'ninos/:id/editar', component: NinoForm },


      /* =======================================
         🔵 RUTAS EXISTENTES DEL SISTEMA
         ======================================= */
      { path: 'citas', component: Citas },
      { path: 'usuarios', component: Usuarios },
      { path: 'terapias', component: Terapias },
      { path: 'perfil', component: Perfil },
      { path: 'configuracion', component: Configuracion },

      /* Ruta por defecto */
      { path: '', redirectTo: 'citas', pathMatch: 'full' },
    ],
  },
];
